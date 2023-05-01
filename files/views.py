from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from .models import Item, Image
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import ItemCreateForm, ItemUpdateForm
from django.shortcuts import get_object_or_404
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin


class ItemCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create a new item after validation.
    user will be auto set.
    send success message and redirect to home.
    """
    model = Item
    form_class = ItemCreateForm
    template_name = 'files/create.html'
    success_message = "فایل با موفقیت ساخته شد ! (پس از بررسی منتشر خواهد شد)"
    success_url = reverse_lazy('home:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        item_code = form.instance.code
        images = self.request.FILES.getlist('img')
        item_data = form.save()

        # create image and limits
        i = 0
        if images:
            with transaction.atomic():
                for img in images:
                    if i <= 5 and img.size < 600000:
                        image = Image.objects.create(code=item_code, image=img)
                        image.save()
                        i += 1

            self.request.session['add_image'] = {
                'code': item_code
            }

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_items = Item.objects \
            .filter(user__exact=self.request.user) \
            .order_by('-created')
        publish_items = all_items.filter(publish=True)
        public_items = publish_items.filter(public=True)

        a, psh, pc = 0, 0, 0
        for item in all_items:
            a += 1

        for item in publish_items:
            psh += 1

        for item in public_items:
            pc += 1

        context['all_user_items'] = a
        context['publish_items'] = psh
        context['public_items'] = pc

        return context


class ItemDetailView(DetailView):
    """
    Show items detail.
    """
    template_name = 'files/detail.html'
    context_object_name = 'item'

    def get(self, request, *args, **kwargs):
        item_code = self.kwargs['code']
        self.item_images = None
        if item_code:
            self.item_images = self.get_object().images
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(Item, code__exact=self.kwargs['code'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hit_count = get_hitcount_model().objects.get_for_object(self.get_object())
        hits = hit_count.hits
        hit_count_response = HitCountMixin.hit_count(self.request, hit_count)
        if hit_count_response.hit_counted:
            hits = hits + 1

        if self.get_object().all_price:
            context['price_per_meter'] = round(self.get_object().all_price / self.get_object().area)

        all_items = Item.objects\
                .filter(user_id__exact=self.get_object().user.id)\
                .filter(publish=True)
        a = 0
        for item in all_items:
            a += 1

        context['all_user_items'] = a
        context['item_images'] = self.item_images
        context['object'] = self.get_object()
        return context


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete an Item and Images.
    just item owner can do.
    """
    model = Item
    template_name = 'files/delete_item.html'

    def dispatch(self, request, *args, **kwargs):
        messages.error(request, "فایل مورد نظر با موفقیت حذف شد !", 'danger')
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
    success_message = "فایل مورد نظر با موفقیت ویرایش شد ! (پس از بررسی منتشر خواهد شد)"
    success_url = reverse_lazy('home:home')

    def get(self, request, *args, **kwargs):
        self.item_images = None
        item_code = self.kwargs['code']
        if item_code:
            self.item_images = self.get_queryset().images.all()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        item = self.get_queryset()
        item.publish = False
        item.save()
        return super(ItemUpdateView, self).post(self, request, *args, **kwargs)

    def form_valid(self, form):
        images = self.request.FILES.getlist('img')
        item_code = self.kwargs['code']
        item_images = self.get_queryset().images.all()

        # image limit
        i = 0
        if item_images:
            for img in item_images:
                i += 1

        if images:
            with transaction.atomic():
                for img in images:
                    if i <= 5 and img.size < 600000:
                        image = Image.objects.create(code=item_code, image=img)
                        image.save()
                        i += 1
            self.request.session['add_image'] = {
                'code': item_code
            }
        return super().form_valid(form)

    def get_queryset(self):
        return get_object_or_404(Item, code__exact=self.kwargs['code'])

    def get_object(self, queryset=None):
        obj = Item.objects.get(code__exact=self.get_queryset().code)
        return obj if obj.user == self.request.user else None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_images = self.get_queryset().images.all()

        # image limit
        i = 0
        if item_images:
            for img in item_images:
                i += 1

        context["item_images"] = item_images
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
        messages.error(request, "تصویر مورد نظر با موفقیت حذف شد !", 'danger')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Image.objects.filter(code__exact=self.kwargs['code'])

    def get_object(self, queryset=None):
        img = self.get_queryset()
        for i in img:
            img_user = Item.objects.get(code__exact=i.code).user
            if img_user == self.request.user:
                i.delete()
        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = Item.objects.get(code__exact=self.kwargs['code'])
        return context

