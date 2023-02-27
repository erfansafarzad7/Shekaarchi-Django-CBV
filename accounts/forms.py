from django import forms
from .models import User, Otp
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    """
    User creation form.
    check passwords match and set password.
    """
    password = forms.CharField(required=True, label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'phone', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    User edit form.
    edit password link.
    """
    password = ReadOnlyPasswordHashField(help_text=
                                         "You Can Change The Password Using <a href=\"../password/\">This Form</a>.")

    class Meta:
        model = User
        fields = ('username', 'phone', 'email', 'password', 'last_login')


class VerifyForm(forms.ModelForm):
    """
    Verify otp code.
    """
    class Meta:
        model = Otp
        fields = ('code', )
