from django.db import models
from ckeditor.fields import RichTextField


class Item(models.Model):
    code = models.CharField(max_length=7)
    image = models.ImageField(null=True)
    address = models.TextField(max_length=250)
    area = models.PositiveIntegerField()
    foundation = models.PositiveIntegerField()
    floor = models.PositiveSmallIntegerField(null=True, blank=True)
    bedroom = models.PositiveSmallIntegerField(null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    all_price = models.CharField(max_length=15)
    owner = models.CharField(max_length=30)
    owner_info = models.TextField(max_length=200)
    description = RichTextField()
    deed = models.BooleanField(default=False)
    exchange = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    # Item Options
    points = models.BooleanField(default=False)
    mdf = models.BooleanField(default=False)
    cooler = models.BooleanField(default=False)
    heating = models.BooleanField(default=False)
    water_heater = models.BooleanField(default=False)
    elevator = models.BooleanField(default=False)
    video_intercom = models.BooleanField(default=False)
    remote_door = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    warehouse = models.BooleanField(default=False)




