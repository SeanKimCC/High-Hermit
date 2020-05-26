from django.contrib import admin

# Register your models here.
from .models import Product, Brand, Site

admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Site)
