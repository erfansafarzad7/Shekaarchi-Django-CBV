from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='user_profile'),
    path('edit-profile/<int:pk>/', views.UserEditProfileView.as_view(), name='edit_profile'),

]

