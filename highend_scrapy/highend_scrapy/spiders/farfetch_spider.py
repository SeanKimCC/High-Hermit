import scrapy
from scrapy.http.request import Request
from highend_scrapy.items import ProductItem, BrandItem, SiteItem, PriceHistoryItem, ProductStockItem
from main.models.models import Product, Brand, Site, PriceHistory, ProductStock
from main.models.CategoryModel import Category
from random import randint
from scraper_api import ScraperAPIClient
import datetime
import json

class FarfetchSpider(scrapy.Spider):
	name = "farfetch"

	def start_requests(self):
		for brandName in brandNames:
			print(f'SCRAPING {brandName}')
			for category in categories:
				print(f'	SCRAPING {category}')
				data = {'brandName': brandName, 'category': category}
				yield scrapy.Request(client.scrapyGet(url=f'https://www.farfetch.com/ca/shopping/men/{brandName}/{category}'), meta=data)


	def parse(self, response):
		# links = response.xpath("//img/@data-srcset")
		product_prices = response.xpath("//span[@data-test='price']/text()").extract()
		product_names = response.xpath("//p[@data-test='productDescription']/text()").extract()

		# html = ""

		# for link in links:
		# 	url = link.get()

		# 	if any(extension in url for extension in ['.jpg', '.gif', '.png']):
		# 		html += """<a href="{url}"
		# 		target="_blank">
		# 		<img src="{url}" height="33%"
		# 		width="33%"/>
		# 		</a>""".format(url=url)

		# 		with open("frontpage.html", "a") as page:
		# 			page.write(html)
		# 			page.close()

		# print(product_names)
		# print(product_prices)

		# print(len(product_names), len(product_prices))
		loopLen = min(len(product_names), len(product_prices))
		for i in range(loopLen):
			s = ''.join(x for x in product_prices[i] if x.isdigit())
			product_prices[i] = int(s)
			product_names[i] = product_names[i].strip()

		acne_brand, brand_created = Brand.objects.get_or_create(name="Acne Studios")
		acne_brand.save()

		farfetch_site, site_created = Site.objects.get_or_create(name="Farfetch", link="https://www.farfetch.com/")
		farfetch_site.save()
		# print(Brand.objects.all())



		for i in range(loopLen):
			p, created = Product.objects.update_or_create(product_name=product_names[i], 
				defaults={'sale_price': product_prices[i],\
				'brand': acne_brand, 'associated_site': farfetch_site})

			if(created):
				print("created")
			# p = Product.objects.update_or_create(product_name=product_names[i], sale_price=product_prices[i],\
			# 	brand=acne_brand, associated_site=ssense_site)
			p.save()
