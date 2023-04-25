from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import UpdateView, ListView, FormView, DeleteView
from django.db import transaction
from files.models import Item
from .models import User, Otp
from .forms import UserCreationForm, SMSVerifyForm, GetPhoneForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from utils import send_sms
from random import randint
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from .custom_auth import auth as c_auth
import datetime


class LoginView(SuccessMessageMixin, LoginView):
    """
    Login and send success message.
    """
    template_name = 'accounts/login.html'
    success_message = "با موفقیت وارد شدید !"
    next_page = reverse_lazy('home:home')


class OtpLoginView(SuccessMessageMixin, FormView):
    """
    Login with otp.
    """
    template_name = 'accounts/get_phone.html'
    form_class = GetPhoneForm
    success_message = "کد یکبار مصرف را وارد کنید !"
    success_url = reverse_lazy('accounts:sms_verify')

    def get(self, request, *args, **kwargs):
        messages.info(self.request, "شماره تلفن خود را وارد کنید !", 'info')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Get phone and send to sms verification view.
        """
        phone = form.cleaned_data.get('phone')
        now = datetime.datetime.now()

        # create random code for otp
        rnd_code = randint(1000, 9999)

        self.request.session['login_with_otp'] = {
            'entered_phone': phone
        }
        self.request.session['user_info'] = {
            'phone': phone,
            'rnd_code': rnd_code
        }
        self.request.session['request_timer'] = {
            'now': str(now)
        }

        return super(OtpLoginView, self).form_valid(form)


class LogoutView(LoginRequiredMixin, LogoutView):
    """
    Logout view.
    """
    next_page = reverse_lazy('home:home')

    def dispatch(self, request, *args, **kwargs):
        messages.warning(request, "با موفقیت خارج شدید !", 'warning')
        return super().dispatch(request, *args, **kwargs)


class RegisterView(SuccessMessageMixin, FormView):
    """
    Register form for new user and send to sms verification view..
    """
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    success_message = "کد یکبار مصرف را وارد کنید !"
    success_url = reverse_lazy('accounts:sms_verify')

    def form_valid(self, form):
        """
        Create user register info session.
        """
        cd = form.cleaned_data
        phone, username, password = cd.get('phone'), cd.get('username'), cd.get('password')
        now = datetime.datetime.now()

        # create random code for otp
        rnd_code = randint(1000, 9999)

        # user register session
        self.request.session['user_register_info'] = {
            'phone': phone,
            'username': username,
            'password': password,
        }

        self.request.session['user_info'] = {
            'phone': phone,
            'rnd_code': rnd_code
        }
        self.request.session['request_timer'] = {
            'now': str(now)
        }

        return super(RegisterView, self).form_valid(form)


class UserProfileView(LoginRequiredMixin, ListView):
    """
    Show users profile and posts.
    Users can edit profile and delete/edit post if it's their own.
    """
    template_name = 'accounts/user_profile.html'
    model = Item

    def get(self, request, *args, **kwargs):
        self.items_user = get_object_or_404(User, id=kwargs['pk'])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_items = Item.objects.filter(user_id__exact=self.kwargs['pk'])
        publish_items = all_items.filter(publish=True)
        public_items = publish_items.filter(public=True)

        if self.request.user.id == self.items_user.id:
            context["items"] = all_items.order_by('-updated')
        else:
            context["items"] = all_items.exclude(publish__exact=False).order_by('-updated')

        a, psh, pc = 0, 0, 0
        for item in all_items:
            a += 1

        for item in publish_items:
            psh += 1

        for item in public_items:
            pc += 1

        context['all_user_items'] = a
        context['publish_items'] = psh
        context['public_items'] = pc
        context['items_user'] = self.items_user

        return context


class UserEditProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    User can edit just own info.
    """
    template_name = 'accounts/edit_profile.html'
    model = User
    fields = ('username', 'address', 'avatar')
    context_object_name = 'user'
    success_message = "تغییرات پس از تایید ثبت خواهند شد !"
    success_url = reverse_lazy('home:home')

    def get(self, request, *args, **kwargs):
        self.avatar = None
        user_id = self.kwargs['pk']
        if user_id:
            self.avatar = self.get_object().avatar
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        user.show_avatar = False
        user.save()
        return super().post(self, request, *args, **kwargs)

    def get_queryset(self):
        return get_object_or_404(User, id=self.kwargs['pk'])

    def get_object(self, queryset=None):
        obj = User.objects.get(id=self.get_queryset().id)
        return obj if obj.id == self.request.user.id else None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_items = Item.objects.filter(user_id__exact=self.kwargs['pk'])
        publish_items = all_items.filter(publish=True)
        public_items = publish_items.filter(public=True)

        if self.request.user.id == self.get_queryset().id:
            context["items"] = all_items
        else:
            context["items"] = all_items.exclude(publish__exact=False)

        a, psh, pc = 0, 0, 0
        for item in all_items:
            a += 1

        for item in publish_items:
            psh += 1

        for item in public_items:
            pc += 1

        context['all_user_items'] = a
        context['publish_items'] = psh
        context['public_items'] = pc
        context['items_user'] = self.get_queryset()

        return context

    def form_valid(self, form):
        avatar = self.request.FILES.get('avatar')
        user = self.get_object()
        print(avatar, user)

        if avatar and avatar.size < 1000000:
            with transaction.atomic():
                user.avatar = avatar
                user.save()

        return super(UserEditProfileView, self).form_valid(form)


class DeleteAvatarView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'accounts/delete_avatar.html'

    def dispatch(self, request, *args, **kwargs):
        messages.error(request, "تصویر مورد نظر با موفقیت حذف شد !", 'danger')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return get_object_or_404(User, id=self.kwargs['pk'])

    def get_object(self, queryset=None):
        avatar = self.get_queryset().avatar
        if self.get_queryset() == self.request.user:
            avatar.delete()
        return True


class EditPhoneView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    """
    New Phone Form View.
    """
    template_name = 'accounts/get_phone.html'
    form_class = GetPhoneForm
    success_message = "کد یکبار مصرف را وارد کنید !"
    success_url = reverse_lazy('accounts:sms_verify')

    def get(self, request, *args, **kwargs):
        messages.info(self.request, "Enter New Phone Number", 'info')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Get new phone and send to sms verification view.
        """
        new_phone = form.cleaned_data.get('phone')
        now = datetime.datetime.now()

        # create random code for otp
        rnd_code = randint(1000, 9999)

        self.request.session['user_change_phone'] = {
            'user_id': self.request.user.id,
            'phone': new_phone
        }
        self.request.session['user_info'] = {
            'phone': new_phone,
            'rnd_code': rnd_code
        }
        self.request.session['request_timer'] = {
            'now': str(now)
        }

        return super(EditPhoneView, self).form_valid(form)


class SMSVerifyView(SuccessMessageMixin, FormView):
    """
    Verify with sms before changes.
    """
    template_name = 'accounts/sms_verify.html'
    form_class = SMSVerifyForm
    success_url = reverse_lazy('home:home')

    def get(self, request, *args, **kwargs):
        """
        Create otp and send sms.
        """
        now = datetime.datetime.now()
        delay = now + datetime.timedelta(minutes=2)
        session = self.request.session
        session['request_timer']['delay'] = str(delay)
        user_info = session['user_info']
        rnd_code = user_info['rnd_code']
        session_timer = session['request_timer']
        user_phone = None

        if 'user_info' in session:
            user_phone = user_info['phone']

        otp = Otp.objects.filter(code__exact=rnd_code).exists()

        if not otp and session_timer['now'] < session_timer['delay']:
            Otp.objects.create(phone=user_phone, code=rnd_code)
            # send code with sms
            text = f" shekaarchi.ir \n کد یکبار مصرف شما : {rnd_code} \n لغو پیامک:۱۱ "
            send_sms(user_phone, text)

        return super(SMSVerifyView, self).get(self, request, *args, **kwargs)

    def form_valid(self, form):
        """
        Register new user or change phone number after sms verification.
        """
        try:
            entered_otp = form.cleaned_data.get('code')
            user_session = self.request.session
            otp = Otp.objects.get(code__exact=entered_otp)

            if entered_otp == otp.code:
                # for user change phone
                if 'user_change_phone' in user_session:
                    user_session = self.request.session['user_change_phone']
                    user = User.objects.get(id=user_session['user_id'])
                    if self.request.user == user:
                        user.phone = user_session['phone']
                        user.save()
                        otp.delete()
                        del user_session
                        return super(SMSVerifyView, self).form_valid(form)

                # for user register
                if 'user_register_info' in user_session:
                    user_session = self.request.session['user_register_info']
                    if user_session['phone'] == otp.phone:
                        User.objects.create_user(phone=user_session['phone'],
                                                 email=user_session['email'],
                                                 username=user_session['username'],
                                                 password=user_session['password'],
                                                 )
                        new_user = authenticate(phone=user_session['phone'], password=user_session['password'])
                        login(self.request, new_user)
                        otp.delete()
                        del user_session
                        return super(SMSVerifyView, self).form_valid(form)

                # for user login with otp
                if 'login_with_otp' in user_session:
                    user_session = self.request.session['login_with_otp']
                    user = User.objects.get(phone__exact=user_session['entered_phone'])

                    # custom auth
                    auth_user = c_auth.authenticate(phone=user.phone, otp_code=otp.code)

                    login(self.request, auth_user)
                    otp.delete()
                    del user_session
                    return super(SMSVerifyView, self).form_valid(form)

        except ObjectDoesNotExist:
            messages.warning(self.request, "کد اشتباه است !", 'warning')
            return redirect('accounts:sms_verify')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["e_phone"] = self.request.session['user_info']['phone']
        return context

