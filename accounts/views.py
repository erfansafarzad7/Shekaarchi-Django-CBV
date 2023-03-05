from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import UpdateView, ListView, FormView
from files.models import Item
from .models import User, Otp
from .forms import UserCreationForm, SMSVerifyForm, GetPhoneForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from utils import send_sms
from random import randint
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from .custom_auth import authenticate


class LoginView(SuccessMessageMixin, LoginView):
    """
    Login and send success message.
    """
    template_name = 'accounts/login.html'
    success_message = "You Have Successfully logged In!"
    next_page = reverse_lazy('home:home')


class OtpLoginView(SuccessMessageMixin, FormView):
    """
    Login with otp.
    """
    template_name = 'accounts/get_phone.html'
    form_class = GetPhoneForm
    success_message = "Enter Otp"
    success_url = reverse_lazy('accounts:sms_verify')

    def get(self, request, *args, **kwargs):
        messages.info(self.request, "Enter Phone Number", 'info')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Get phone and send to sms verification view.
        """
        phone = form.cleaned_data.get('phone')
        self.request.session['login_with_otp'] = {
            'entered_phone': phone
        }
        self.request.session['user_info'] = {
            'phone': phone
        }

        return super(OtpLoginView, self).form_valid(form)


class LogoutView(LoginRequiredMixin, LogoutView):
    """
    Logout view.
    """
    next_page = reverse_lazy('home:home')

    def dispatch(self, request, *args, **kwargs):
        messages.warning(request, "You Have Successfully logged Out!", 'warning')
        return super().dispatch(request, *args, **kwargs)


class RegisterView(SuccessMessageMixin, FormView):
    """
    Register form for new user and send to sms verification view..
    """
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    success_message = "Enter Otp On SMS!"
    success_url = reverse_lazy('accounts:sms_verify')

    def form_valid(self, form):
        """
        Create user register info session.
        """
        cd = form.cleaned_data
        phone, email, username, password = cd.get('phone'), cd.get('email'), cd.get('username'), cd.get('password')

        # user register session
        self.request.session['user_register_info'] = {
            'phone': phone,
            'email': email,
            'username': username,
            'password': password,
        }

        self.request.session['user_info'] = {
            'phone': phone,
        }

        return super(RegisterView, self).form_valid(form)


class UserProfileView(LoginRequiredMixin, ListView):
    """
    Show users profile and posts.
    Users can edit profile and delete/edit post if it's their own.
    """
    template_name = 'accounts/user_profile.html'
    model = Item
    context_object_name = 'items'
    paginate_by = 10

    def get_queryset(self):
        return Item.objects.filter(user__exact=self.kwargs['pk']).order_by('-created')

    def get(self, request, *args, **kwargs):
        self.items_user = get_object_or_404(User, id=kwargs['pk'])
        return super().get(request, *args, **kwargs) if self.items_user == request.user else None

    def get_context_data(self, **kwargs):
        return super().get_context_data(items_user=self.items_user.id, **kwargs)


class UserEditProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    User can edit just own info.
    """
    template_name = 'accounts/edit_profile.html'
    model = User
    fields = ('username',)
    context_object_name = 'user'
    success_message = "Your Profile Successfully Edited!"
    success_url = reverse_lazy('home:home')

    def get_queryset(self):
        return get_object_or_404(User, id=self.kwargs['pk'])

    def get_object(self, queryset=None):
        obj = User.objects.get(id=self.get_queryset().id)
        return obj if obj.id == self.request.user.id else None


class EditPhoneView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    """
    New Phone Form View.
    """
    template_name = 'accounts/get_phone.html'
    form_class = GetPhoneForm
    success_message = "Enter Otp"
    success_url = reverse_lazy('accounts:sms_verify')

    def get(self, request, *args, **kwargs):
        messages.info(self.request, "Enter New Phone Number", 'info')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Get new phone and send to sms verification view.
        """
        new_phone = form.cleaned_data.get('phone')
        self.request.session['user_change_phone'] = {
            'user_id': self.request.user.id,
            'phone': new_phone
        }
        self.request.session['user_info'] = {
            'phone': new_phone
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

        # add timer

        user_phone = None
        if 'user_info' in self.request.session:
            user_phone = self.request.session['user_info']['phone']

        # create otp code
        rnd_code = randint(1000, 9999)
        Otp.objects.create(phone=user_phone, code=rnd_code)

        # send code with sms
        text = f" shekaarchi.ir \n ur code is : {rnd_code} \n لغو پیامک:۱۱ "
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
                    auth_user = authenticate.custom_auth(phone=user.phone, otp_code=otp.code)

                    login(self.request, auth_user)
                    otp.delete()
                    del user_session
                    return super(SMSVerifyView, self).form_valid(form)

        except ObjectDoesNotExist:
            messages.warning(self.request, "There Is A Problem!", 'warning')
            return redirect('accounts:sms_verify')

