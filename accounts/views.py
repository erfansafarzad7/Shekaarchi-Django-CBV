from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy
from django.contrib.messages import views as message


class LoginView(message.SuccessMessageMixin, auth_view.LoginView):
    """
    Login and send success message.
    """
    template_name = 'accounts/login.html'
    success_message = 'Successfully logged In!'
    next_page = reverse_lazy('home:home')


class LogoutView(auth_view.LogoutView):
    """
    Logout view.
    """
    next_page = reverse_lazy('home:home')
