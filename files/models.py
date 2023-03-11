from django.db import models
from accounts.models import User


class Image(models.Model):
    code = models.BigIntegerField(unique=False)
    image = models.ImageField()
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code}"


class Item(models.Model):
    """
    Item model.
    item code is unique.
    required fields : (user, code, type, address, area, all_price, owner, owner_info)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='item_user')
    images = models.ManyToManyField(Image, related_name='item_images')
    code = models.BigIntegerField(unique=True, verbose_name='کد')
    publish = models.BooleanField(default=False, verbose_name='انتشار')
    public = models.BooleanField(default=True, verbose_name='نمایش عمومی')

    subject = models.CharField(max_length=10, null=False, blank=False, verbose_name='موضوع',
                               choices=[('sell', 'فروش'),
                                        ('mortgage', 'رهن'),
                                        ('rent', 'اجاره'), ])

    type = models.CharField(max_length=10, verbose_name='نوع', null=False, blank=False,
                            choices=[('land', 'زمین'),
                                     ('house', 'خانه'), ])

    land_type = models.CharField(max_length=15, null=True, blank=True, verbose_name='نوع زمین',
                                 choices=[('residential', 'مسکونی'),
                                          ('commercial', 'تجاری'),
                                          ('res_comm', 'مسکونی - تجاری'),
                                          ('garden', 'باغی'),
                                          ('rice_field', 'کشاورزی'), ])

    house_type = models.CharField(max_length=15, null=True, blank=True,
                                  choices=[('villa', 'ویلا'), ('apartment', 'اپارتمان')], verbose_name='نوع خانه')

    rice_field_type = models.CharField(max_length=15, null=True, blank=True, verbose_name='نوع زمین کشاورزی',
                                       choices=[('mechanized', 'مکانیزه'),
                                                ('traditional', 'سنتی'), ])

    # required fields
    address = models.TextField(max_length=250, verbose_name='آدرس')
    city = models.CharField(max_length=20, verbose_name='شهر/محل', null=True, blank=True)
    area = models.PositiveIntegerField(verbose_name='متراژ')
    all_price = models.BigIntegerField(verbose_name='قیمت کل')
    rent_price = models.BigIntegerField(verbose_name='بیعانه', null=True, blank=True)
    owner = models.CharField(max_length=30, verbose_name='نام مالک')
    owner_info = models.TextField(max_length=200, verbose_name='مشخصات مالک')

    documents = models.CharField(max_length=15, null=True, blank=True, verbose_name='مدرک',
                                 choices=[('deed', 'سند دار'),
                                          ('nasaq', 'نسق'),
                                          ('arrangement', 'قولنامه ای')])
    exchange = models.BooleanField(default=False, verbose_name='معاوضه')
    inside_plan = models.BooleanField(default=False, verbose_name='داخل طرح')
    points = models.BooleanField(default=False, verbose_name='امتیازات')

    # house options
    foundation = models.PositiveIntegerField(null=True, blank=True, verbose_name='زیربنا')
    floor = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='طبقه')
    bedroom = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='تعداد اتاق خواب')
    year = models.PositiveIntegerField(null=True, blank=True, verbose_name='سال ساخت')
    mdf = models.BooleanField(default=False, verbose_name='ام دی اف')
    cooler = models.BooleanField(default=False, verbose_name='کولر')
    water_heater = models.BooleanField(default=False, verbose_name='آبگرمکن')
    elevator = models.BooleanField(default=False, verbose_name='اسانسور')
    video_intercom = models.BooleanField(default=False, verbose_name='آیفون تصویری')
    remote_door = models.BooleanField(default=False, verbose_name='درب ریموت دار')
    parking = models.BooleanField(default=False, verbose_name='پارکینگ')
    warehouse = models.BooleanField(default=False, verbose_name='بهار خواب')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات')

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code}"




