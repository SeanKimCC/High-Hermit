from django.contrib import admin

# Register your models here.
from .models import Product, Brand, Site



class ProductInline(admin.TabularInline):
    model = Product

class BrandAdmin(admin.ModelAdmin):
    model = Brand
    inlines = [
        ProductInline,
    ]


admin.site.register(Product)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Site)