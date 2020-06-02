from rest_framework import serializers
from .models import Product, Brand

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('unique_id', 'name')


class ProductSerializer(serializers.ModelSerializer):
	brand_name = serializers.CharField(source='brand.name')
	class Meta:
		model = Product
		fields = ('unique_id', 'product_name', 'brand_name', 'sale_price')