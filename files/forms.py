from django import forms
from .models import Item
from accounts.models import User
from django.forms import inlineformset_factory


class ItemCreateForm(forms.ModelForm):
    """
    Create item form.
    user field will be set automatically.
    """
    img = forms.ImageField(allow_empty_file=True)

    class Meta:
        model = Item
        fields = '__all__'
        exclude = ('user', 'images')


class ItemUpdateForm(forms.ModelForm):
    """
    Update item form.
    can't edit code and user.
    """

    class Meta:
        model = Item
        fields = '__all__'
        exclude = ('user', 'code')


# class ItemImageForm(forms.ModelForm):
#
#     class Meta:
#         model = ItemImage
#         fields = '__all__'

#
# ItemImageFormSet = inlineformset_factory(
#     Item, ItemImage, form=ItemImageForm, fields=['image'], extra=3, can_delete=True
# )

