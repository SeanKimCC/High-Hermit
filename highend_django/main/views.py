from django.shortcuts import render
import requests


# Create your views here.
from main.models.models import Brand, Product, PriceHistory
from main.serializers import BrandSerializer, ProductSerializer, PriceHistorySerializer
from rest_framework import viewsets
from rest_framework.response import Response

# from rest_framework import generics

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # def get_queryset(self):
    # 	# if(request.GET.get('brandName')):
    # 	# 	return Product.objects.filter(brand=request.GET.get('brandName')))
    # 	# return Product.objects.all();

    # 	# original qs
    #     qs = super().get_queryset() 
    #     # filter by a variable captured from url, for example
    #     print(self, self.kwargs)
    #     print(kwargs)
    #     # if(self.kwargs['brandName']):
    #    	# 	return qs.filter(brand=self.kwargs['brandName'])
    #    	# return 
    def list(self, request):
    	queryset = self.queryset
    	

    	if(request.GET.get('brandName')):
    		queryset=self.queryset.filter(brand__name=request.GET.get('brandName'))

    	page = self.paginate_queryset(queryset)
    	if page is not None:
    		serializer = ProductSerializer(page, many=True)
    	else:
    		serializer = ProductSerializer(queryset, many=True)
    	return Response(serializer.data)
		# serializer = ProductSerializer(queryset)
		# serializer=ProductSerializer(queryset)

		# serializer = ProductSerializer(queryset)

		# return Response(serializer.data)

class PriceHistoryViewSet(viewsets.ModelViewSet):
    queryset = PriceHistory.objects.all()
    serializer_class = PriceHistorySerializer
    
    def list(self, request):
        queryset = self.queryset
        if (request.GET.get('productId')):
            queryset = self.queryset.filter(product__unique_id=request.GET.get('productId'))

        serializer = PriceHistorySerializer(queryset, many=True)
        return Response(serializer.data)

