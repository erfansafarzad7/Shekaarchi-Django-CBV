from django import forms
from .models import Item
from accounts.models import User


class ItemCreateForm(forms.ModelForm):
    """
    Create item form.
    user field will be set automatically.
    """

    class Meta:
        model = Item
        fields = '__all__'
        exclude = ('user', )


class ItemUpdateForm(forms.ModelForm):
    """
    Update item form.
    can't edit code and user.
    """

    class Meta:
        model = Item
        fields = '__all__'
        exclude = ('user', 'code')

