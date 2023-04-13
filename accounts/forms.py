from django import forms
from .models import User, Otp
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    """
    User creation form.
    check passwords match and set password.
    """
    password = forms.CharField(min_length=6, max_length=20, required=True, label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'phone')

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
        fields = '__all__'


class SMSVerifyForm(forms.ModelForm):
    """
    Verify otp code.
    """
    class Meta:
        model = Otp
        fields = ('code', )


class GetPhoneForm(forms.Form):
    phone = forms.CharField()

