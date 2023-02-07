from django.db import models
from ckeditor.fields import RichTextField
from accounts.models import User


class Item(models.Model):
    """
    Item model.
    item code is unique.
    required fields : (user, code, type, address, area, all_price, owner, owner_info)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='item_user')
    code = models.BigIntegerField(unique=True)
    type = models.CharField(max_length=100, choices=[('land', 'land'), ('house', 'house')])
    image = models.ImageField(null=True, blank=True)
    address = models.TextField(max_length=250)
    area = models.PositiveIntegerField()
    foundation = models.PositiveIntegerField(null=True, blank=True)
    floor = models.PositiveSmallIntegerField(null=True, blank=True)
    bedroom = models.PositiveSmallIntegerField(null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    all_price = models.BigIntegerField()
    owner = models.CharField(max_length=30)
    owner_info = models.TextField(max_length=200)
    description = RichTextField(null=True, blank=True)

    # Item Details
    deed = models.BooleanField(default=False)
    exchange = models.BooleanField(default=False)
    residential = models.BooleanField(default=False)
    garden = models.BooleanField(default=False)
    commercial = models.BooleanField(default=False)
    rice_field = models.BooleanField(default=False)
    mechanized = models.BooleanField(default=False)
    traditional = models.BooleanField(default=False)
    inside_plan = models.BooleanField(default=False)
    points = models.BooleanField(default=False)

    # Item Options
    house_type = models.CharField(max_length=100, choices=[('villa', 'villa'), ('apartment', 'apartment')], null=True, blank=True)

    mdf = models.BooleanField(default=False)
    cooler = models.BooleanField(default=False)
    heating = models.BooleanField(default=False)
    water_heater = models.BooleanField(default=False)
    elevator = models.BooleanField(default=False)
    video_intercom = models.BooleanField(default=False)
    remote_door = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    warehouse = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code}"

