from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.
    """
    phone = models.CharField(max_length=11, unique=True, verbose_name='شماره تماس ')
    username = models.CharField(max_length=25, unique=True, verbose_name='نام املاک ')
    avatar = models.ImageField(upload_to="avatars", verbose_name='آواتار', null=True, blank=True)
    show_avatar = models.BooleanField(default=False, verbose_name='نمایش عکس پروفایل')
    address = models.CharField(max_length=100, verbose_name='آدرس ', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return f'{self.username}'

    @property
    def is_staff(self):
        return self.is_admin


class Otp(models.Model):
    """
    Otp code for register/login and forget password.
    """
    phone = models.CharField(max_length=11)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone} - {self.code}"
