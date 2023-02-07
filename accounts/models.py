from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.
    """
    phone_number = models.CharField(max_length=11, unique=True)
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('phone_number', 'email')

    def __str__(self):
        return f'{self.username} -- {self.phone_number}'

    @property
    def is_staff(self):
        return self.is_admin

