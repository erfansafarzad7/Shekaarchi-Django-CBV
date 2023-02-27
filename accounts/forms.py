from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    """
    User creation form.
    check passwords match and set password.
    """
    password1 = forms.CharField(required=True, label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(required=True, label='Password2', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'email')

    def clean_pass(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError("Passwords Doesn't Match!")
        return cd['password1']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
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
        fields = ('username', 'phone_number', 'email', 'password', 'last_login')


class VerifyForm(forms.ModelForm):
    """
    Verify otp code.
    """
    class Meta:
        model = Otp
        fields = ('code', )
