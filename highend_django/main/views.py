from django.shortcuts import render

# Create your views here.
from main.models import Brand, Product
from main.serializers import BrandSerializer, ProductSerializer
from rest_framework import viewsets

# from rest_framework import generics

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer