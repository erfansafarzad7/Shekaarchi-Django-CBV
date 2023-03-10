from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from .models import Item, Image
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import ItemCreateForm, ItemUpdateForm
from bucket import bucket
from django.shortcuts import get_object_or_404


class ItemCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create a new item after validation.
    user will be auto set.
    send success message and redirect to home.
    """
    model = Item
    form_class = ItemCreateForm
    template_name = 'files/create.html'
    success_message = "Item Successfully Created"
    success_url = reverse_lazy('home:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        item_code = form.instance.code
        images = self.request.FILES.getlist('img')
        item_data = form.save()

        # image limit
        i = 0
        for img in images:
            i += 1

        # Save the images
        if images and i <= 5:
            with transaction.atomic():
                for image in images:
                    img = Image.objects.create(code=item_code, image=image)
                    img.save()

        return super().form_valid(form)


class ItemDetailView(DetailView):
    """
    Show items detail.
    """
    template_name = 'files/detail.html'
    context_object_name = 'item'

    def get(self, request, *args, **kwargs):
        self.item_images = None
        item_code = self.kwargs['code']
        if item_code:
            self.item_images = Image.objects.filter(code__exact=item_code)
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(Item, code__exact=self.kwargs['code'])

    def get_context_data(self, **kwargs):
        """
        Add context to the template
        """
        return super().get_context_data(item_images=self.item_images, **kwargs)


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete an Item and Images.
    just item owner can do.
    """
    model = Item
    template_name = 'files/delete_item.html'

    def dispatch(self, request, *args, **kwargs):
        messages.error(request, "You Have Successfully Deleted Item!", 'danger')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return get_object_or_404(Item, code=self.kwargs['code'])

    def get_object(self, queryset=None):
        img = Image.objects.filter(code__exact=self.get_queryset().code)
        # if it's users item
        if self.get_queryset().user == self.request.user:
            # delete item
            self.get_queryset().delete()

            if img.exists():
                images = []

                # get all image names
                for i in img:
                    images.append(i.image.name)

                # delete image from bucket
                bucket.delete_object(key=images)
                # delete image from model
                img.delete()
        return True


class ItemUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Edit an Item.
    just item owner can do.
    """
    model = Item
    template_name = 'files/edit_item.html'
    form_class = ItemUpdateForm
    context_object_name = 'item'
    success_message = "Item Successfully Edited!"
    success_url = reverse_lazy('home:home')

    def get(self, request, *args, **kwargs):
        self.item_images = None
        item_code = self.kwargs['code']
        if item_code:
            self.item_images = Image.objects.filter(code__exact=item_code)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        images = self.request.FILES.getlist('img')
        item_code = self.kwargs['code']
        item_images = Image.objects.filter(code__exact=item_code)

        # image limit
        i = 0
        for img in item_images:
            i += 1

        # Save the images
        if images and i <= 5:
            with transaction.atomic():
                for image in images:
                    img = Image.objects.create(code=item_code, image=image)
                    img.save()
        return super().form_valid(form)

    def get_queryset(self):
        return get_object_or_404(Item, code=self.kwargs['code'])

    def get_object(self, queryset=None):
        obj = Item.objects.get(code__exact=self.get_queryset().code)
        return obj if obj.user == self.request.user else None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # image limit
        i = 0
        for img in self.item_images:
            i += 1

        context["item_images"] = self.item_images
        context["range"] = list(range(i, 6))
        return context


class DeleteImageView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    Delete an Images.
    just item owner can do.
    """
    model = Image
    template_name = 'files/delete_image.html'

    def dispatch(self, request, *args, **kwargs):
        messages.error(request, "You Have Successfully Deleted Item!", 'danger')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Image.objects.filter(code__exact=self.kwargs['code'])

    def get_object(self, queryset=None):
        img = self.get_queryset()
        for i in img:
            img_user = Item.objects.get(code__exact=i.code).user
            if img_user == self.request.user:
                if self.kwargs['name'] == i.image.name:
                    # delete image from bucket
                    bucket.delete_object(key=i.image.name)
                    # delete image from model
                    i.delete()
        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = Item.objects.get(code__exact=self.kwargs['code'])
        return context

