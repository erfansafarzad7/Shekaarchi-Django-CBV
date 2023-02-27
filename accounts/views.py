from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import UpdateView, ListView, FormView
from files.models import Item
from .models import User, Otp
from .forms import UserCreationForm, VerifyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from utils import send_sms
from random import randint
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect


class LoginView(SuccessMessageMixin, LoginView):
    """
    Login and send success message.
    """
    template_name = 'accounts/login.html'
    success_message = "You Have Successfully logged In!"
    next_page = reverse_lazy('home:home')


class LogoutView(LoginRequiredMixin, LogoutView):
    """
    Logout view.
    """
    next_page = reverse_lazy('home:home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You Have Successfully logged Out!", 'warning')
        return super().dispatch(request, *args, **kwargs)


class RegisterView(SuccessMessageMixin, FormView):
    """
    Register Form for new user.
    """
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    success_message = "Enter Otp On SMS!"
    success_url = reverse_lazy('accounts:verify')

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

        return super(RegisterView, self).form_valid(form)


class VerifyView(FormView):
    """
    Create and verify otp code and create account.
    """
    template_name = 'accounts/verify.html'
    form_class = VerifyForm
    success_message = "User Successfully Created!"
    success_url = reverse_lazy('home:home')

    def get(self, request, *args, **kwargs):
        """
        Create otp and send sms.
        """
        user_session = self.request.session['user_register_info']
        user_phone = user_session['phone']
        rnd_code = randint(1000, 9999)

        # create otp code
        Otp.objects.create(phone=user_phone, code=rnd_code)

        # send code with sms
        text = f" shekaarchi.ir \n ur code is : {rnd_code} \n لغو پیامک:۱۱ "
        send_sms(user_phone, text)
        return super(VerifyView, self).get(self, request, *args, **kwargs)

    def form_valid(self, form):
        user_session = self.request.session['user_register_info']
        try:
            # get otp and check
            # if it's matches , create account and login
            # else , show message and resend the code
            code = form.cleaned_data.get('code')
            otp = Otp.objects.get(code__exact=code)
            if user_session['phone'] == otp.phone:
                User.objects.create_user(phone=user_session['phone'],
                                         email=user_session['email'],
                                         username=user_session['username'],
                                         password=user_session['password'],
                                         )
                new_user = authenticate(phone=user_session['phone'], password=user_session['password'])
                login(self.request, new_user)
        except ObjectDoesNotExist:
            messages.error(self.request, "otp in wrong! try again", 'warning')
            return redirect('accounts:verify')
        return super(VerifyView, self).form_valid(form)


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
    model = User
    fields = ('username', 'email', 'phone_number')
    template_name = 'accounts/edit_profile.html'
    context_object_name = 'user'
    success_message = "Your Profile Successfully Edited!"
    success_url = reverse_lazy('home:home')

    def get_queryset(self):
        return get_object_or_404(User, id=self.kwargs['pk'])

    def get_object(self, queryset=None):
        obj = User.objects.get(id=self.get_queryset().id)
        return obj if obj.id == self.request.user.id else None

