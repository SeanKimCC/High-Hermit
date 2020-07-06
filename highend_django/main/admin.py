from django.contrib import admin

# Register your models here.
from .models import Product, Brand, Site, PriceHistory, ProductStock


class PriceHistoryInline(admin.TabularInline):
	model = PriceHistory
	list_per_page = 50

class ProductStockInline(admin.TabularInline):
	model = ProductStock
	list_per_page = 50

class ProductAdmin(admin.ModelAdmin):
	model = Product
	list_per_page = 50
	inlines	= [
		PriceHistoryInline,
		ProductStockInline,
	]

class ProductInline(admin.TabularInline):
    model = Product
    list_per_page = 50

class BrandAdmin(admin.ModelAdmin):
    model = Brand
    list_per_page = 50
    inlines = [
        ProductInline,
    ]

class ProductStockAdmin(admin.ModelAdmin):
	model = ProductStock
	list_per_page = 50


admin.site.register(Product, ProductAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Site)
admin.site.register(ProductStock, ProductStockAdmin)