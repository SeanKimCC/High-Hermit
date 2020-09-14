# import scrapy
# from scrapy.http.request import Request
# from highend_scrapy.items import ProductItem, BrandItem, SiteItem, PriceHistoryItem, ProductStockItem
# from main.models.models import Product, Brand, Site, PriceHistory, ProductStock
# from main.models.CategoryModel import Category
# from random import randint
# from scraper_api import ScraperAPIClient
# import datetime
# import json

# client = ScraperAPIClient('95d9c60fead49a8670428a239de1b174')

# brandNames = [line.rstrip() for line in open('../resrc/brand_names.txt')]
# randUAs = [line.rstrip() for line in open('../resrc/rand_user_agents.txt')]
# categories = [line.rstrip() for line in open('../resrc/ssense-categories.txt')]
# base_url = 'http://www.ssense.com/en-ca/men/designers/'

# class SsenseSpider(scrapy.Spider):
# 	name = "ssense-stock"
# 	start_urls = [client.scrapyGet(url=f'http://www.ssense.com/en-ca/men/designers/{brandName}/{category}') for category in categories for brandName in brandNames]

# 	def start_requests(self):
# 		for brandName in brandNames:
# 			print(f'SCRAPING {brandName}')
# 			for category in categories:
# 				print(f'	SCRAPING {category}')
# 				data = {'brandName': brandName, 'category': category}
# 				yield scrapy.Request(client.scrapyGet(url=f'http://www.ssense.com/en-ca/men/designers/{brandName}/{category}'), meta=data)


# 	def parse(self, response):
# 		