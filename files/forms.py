from django import forms
from .models import Item
from accounts.models import User


class ItemCreateForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = '__all__'
        exclude = ('user', )


class ItemUpdateForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = '__all__'
        exclude = ('user', 'code')

