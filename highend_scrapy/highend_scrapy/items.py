# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy_djangoitem import DjangoItem
from main.models import Product, Brand, Site, PriceHistory, ProductStock

class ProductItem(DjangoItem):
	django_model = Product

class BrandItem(DjangoItem):
	django_model = Brand

class SiteItem(DjangoItem):
	django_model = Site

class PriceHistoryItem(DjangoItem):
	django_model = PriceHistory

class ProductStockItem(DjangoItem):
	django_model = ProductStock


# class HighendScrapyItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass
