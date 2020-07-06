import json
import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

# class Currency(models.Model):
# 	official_currency_abbrv = models.CharField(max_length=100, unique=True)

# 	def __str__(self):
# 		return str(self.official_currency_abbrv)


# def default_currency():
#     return Currency.objects.get_or_create(official_currency_abbrv='USD')


# Create your models here.
class Product(models.Model):
    MALE = "M"
    FEMALE = "F"
    UNISEX = "U"
    GENDER_CHOICES = (
        (MALE, 'men'),
        (FEMALE, 'women'),
        (UNISEX, 'unisex'),
    )
    USD = "USD"
    CAD = "CAD"
    KRW = "KRW"
    CURRENCY_CHOICES = (
        ('USD', 'USD'),
        ('CAD', 'CAD'),
        ('KRW', 'KRW'),
    )

    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=300)
    original_price = models.FloatField(null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    web_specific_id = models.CharField(max_length=300)

    sale_price = models.FloatField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    # price_history = models.ForeignKey('PriceHistory', related_name='prices', on_delete=models.SET_NULL, null = True)
    product_link = models.CharField(max_length=500, null=True, default=None)
    product_image = models.CharField(max_length=500, null=True, default=None)
    associated_site = models.ForeignKey('Site', null=True, 
    	on_delete=models.SET_NULL)
    # currency = models.ForeignKey('Currency', default=default_currency(), on_delete=models.SET_DEFAULT)

    item_type = models.CharField(max_length=100, null=True)

    data = models.TextField() # this stands for our crawled data
    date = models.DateTimeField(default=timezone.now)
    
    # This is for basic and custom serialisation to return it to client as a JSON.
    @property
    def to_dict(self):
        data = {
            'data': json.loads(self.data),
            'date': self.date
        }
        return data

    def __str__(self):
        return str(self.product_name)

class ProductStock(models.Model):
    #implement
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    stock_data = ArrayField(models.CharField(max_length=100, null=True))

class Brand(models.Model):
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True, unique=True)

    def __str__(self):
    	return str(self.name)

class Site(models.Model):
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True, unique=True)
    link = models.CharField(max_length=300, null=True)

    def __str__(self):
    	return str(self.name)


class PriceHistory(models.Model):
    USD = "USD"
    CAD = "CAD"
    KRW = "KRW"
    CURRENCY_CHOICES = (
        ('USD', 'USD'),
        ('CAD', 'CAD'),
        ('KRW', 'KRW'),
    )

    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    price = models.FloatField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    date = models.DateField()

    def __str__(self):
        return str(self.product.product_name)

