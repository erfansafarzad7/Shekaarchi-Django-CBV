from django.db import models
from accounts.models import User
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin, HitCount


class Image(models.Model):
    """
    Item images.
    """
    code = models.BigIntegerField(unique=False)
    image = models.ImageField()
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code}"


class Item(models.Model, HitCountMixin):
    """
    Item model.
    item code is unique.
    required fields : (user, code, type, address, area, all_price, owner, owner_info)
    """
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='item_user')
    images = models.ManyToManyField(Image, related_name='item_images', blank=True)
    code = models.PositiveBigIntegerField(unique=True, verbose_name='کد')
    publish = models.BooleanField(default=False, verbose_name='انتشار')
    public = models.BooleanField(default=True, verbose_name='نمایش عمومی')

    subject = models.CharField(max_length=10, null=False, blank=False, verbose_name='موضوع',
                               choices=[('sale', 'فروش'),
                                        ('mortgage', 'رهن'),
                                        ('rent', 'اجاره'), ])

    type = models.CharField(max_length=10, verbose_name='نوع', null=False, blank=False,
                            choices=[('land', 'زمین'),
                                     ('house', 'خانه'),
                                     ('shop', 'مغازه'), ])

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
    state = models.CharField(max_length=20, verbose_name='استان')
    city = models.CharField(max_length=20, verbose_name='شهر/شهرستان')
    village = models.CharField(max_length=20, verbose_name='محل/روستا', null=True, blank=True)
    area = models.PositiveIntegerField(verbose_name='متراژ')
    all_price = models.PositiveBigIntegerField(verbose_name='قیمت کل', null=True, blank=True)
    rent = models.PositiveBigIntegerField(verbose_name='اجاره ', null=True, blank=True)
    all_rent_price = models.PositiveBigIntegerField(verbose_name='ودیعه', null=True, blank=True)
    owner = models.CharField(max_length=30, verbose_name='نام مالک')
    owner_info = models.TextField(max_length=200, verbose_name='مشخصات مالک')

    documents = models.CharField(max_length=15, null=True, blank=True, verbose_name='مدرک',
                                 choices=[('deed', 'سند دار'),
                                          ('nasaq', 'نسق'),
                                          ('arrangement', 'قولنامه ای')])
    exchange = models.BooleanField(default=False, verbose_name='معاوضه')
    inside_plan = models.BooleanField(default=False, verbose_name='داخل طرح')
    points = models.BooleanField(default=False, verbose_name='امتیازات')
    production_license = models.BooleanField(default=False, verbose_name='پروانه ساخت')

    # house options
    foundation = models.PositiveIntegerField(null=True, blank=True, verbose_name='زیربنا')
    floor = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='طبقه')
    bedroom = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='تعداد اتاق خواب')
    year = models.PositiveIntegerField(null=True, blank=True, verbose_name='سال ساخت')
    mdf = models.BooleanField(default=False, verbose_name='ام دی اف')
    ceramic = models.BooleanField(default=False, verbose_name='سرامیک')
    cooler = models.BooleanField(default=False, verbose_name='کولر')
    water_heater = models.BooleanField(default=False, verbose_name='آبگرمکن')
    elevator = models.BooleanField(default=False, verbose_name='اسانسور')
    video_intercom = models.BooleanField(default=False, verbose_name='آیفون تصویری')
    remote_door = models.BooleanField(default=False, verbose_name='درب ریموت دار')
    parking = models.BooleanField(default=False, verbose_name='پارکینگ')
    warehouse = models.BooleanField(default=False, verbose_name='بهار خواب')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات')

    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ آپدیت')

    def __str__(self):
        return f"{self.code}"
