from rest_framework import serializers
from .models.models import Product, Brand, PriceHistory, ProductStock

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('unique_id', 'name')


class ProductSerializer(serializers.ModelSerializer):
	brand_name = serializers.CharField(source='brand.name')
	class Meta:
		model = Product
		fields = ('unique_id', 'product_name', 'brand_name', 'sale_price', 'product_link', 'product_image')

class PriceHistorySerializer(serializers.ModelSerializer):
	product_name = serializers.CharField(source='product.product_name')
	class Meta:
		model = PriceHistory
		fields = ('unique_id', 'product_name', 'price', 'date')

class ProductStockSerializer(serializers.ModelSerializer):
	product_name = serializers.CharField(source='product.product_name')

	class Meta:
		model = ProductStock
		fields = ('unique_id', 'product_name', 'stock_data')