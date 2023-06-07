from django.urls import path
from . import views
from .forms import LoginAuthenticationForm


app_name = 'accounts'
urlpatterns = [
    path('login/', views.LoginView.as_view(form_class=LoginAuthenticationForm), name='login'), # {url 'accounts:login'}
    path('otp-login/', views.OtpLoginView.as_view(), name='otp_login'), # {url 'accounts:otp_login'}
    path('logout/', views.LogoutView.as_view(), name='logout'), # {url 'accounts:logout'}
    path('register/', views.RegisterView.as_view(), name='register'), # {url 'accounts:register'}
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='user_profile'), # {url 'accounts:user_profile' pk}
    path('edit-profile/<int:pk>/', views.UserEditProfileView.as_view(), name='edit_profile'), # {url 'accounts:edit_profile' pk}
    path('delete-avatar/<int:pk>/', views.DeleteAvatarView.as_view(), name='delete_avatar'), # {url 'accounts:delete_avatar' pk}
    path('register/edit-phone/', views.EditPhoneView.as_view(), name='edit_phone'), # {url 'accounts:edit_phone'}
    path('register/sms-verify/', views.SMSVerifyView.as_view(), name='sms_verify'), # {url 'accounts:sms_verify'}

]

