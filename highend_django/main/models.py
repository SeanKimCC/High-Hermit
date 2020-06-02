import json
import uuid

from django.db import models
from django.utils import timezone

# class Currency(models.Model):
# 	official_currency_abbrv = models.CharField(max_length=100, unique=True)

# 	def __str__(self):
# 		return str(self.official_currency_abbrv)


# def default_currency():
#     return Currency.objects.get_or_create(official_currency_abbrv='USD')


# Create your models here.
#past prices can be added for products
class Product(models.Model):
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=300)
    original_price = models.FloatField(null=True)
    sale_price = models.FloatField()
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



