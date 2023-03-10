from django import forms
from .models import Item


class ItemCreateForm(forms.ModelForm):
    """
    Create item form.
    user field will be set automatically.
    """

    class Meta:
        model = Item
        fields = '__all__'
        exclude = ('user', 'images', 'publish', 'public')


class ItemUpdateForm(forms.ModelForm):
    """
    Update item form.
    can't edit code and user.
    """

    class Meta:
        model = Item
        fields = '__all__'
        exclude = ('user', 'code', 'images', 'publish')

