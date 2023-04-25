from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('otp-login/', views.OtpLoginView.as_view(), name='otp_login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='user_profile'),
    path('edit-profile/<int:pk>/', views.UserEditProfileView.as_view(), name='edit_profile'),
    path('delete-avatar/<int:pk>/', views.DeleteAvatarView.as_view(), name='delete_avatar'),
    path('register/edit-phone/', views.EditPhoneView.as_view(), name='edit_phone'),
    path('register/sms-verify/', views.SMSVerifyView.as_view(), name='sms_verify'),

]

