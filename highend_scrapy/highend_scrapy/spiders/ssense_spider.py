import scrapy
import datetime
import json

from scrapy.http.request import Request
from highend_scrapy.items import ProductItem, BrandItem, SiteItem, PriceHistoryItem, ProductStockItem
from main.models.models import Product, Brand, Site, PriceHistory, ProductStock
from main.models.CategoryModel import Category
from random import randint
from scraper_api import ScraperAPIClient
from highend_scrapy.spiders.utils.category_mapping import map_category


client = ScraperAPIClient('95d9c60fead49a8670428a239de1b174')

brandNames = [line.rstrip() for line in open('../resrc/brand_names.txt')]
randUAs = [line.rstrip() for line in open('../resrc/rand_user_agents.txt')]
categories = [line.rstrip() for line in open('../resrc/ssense-categories.txt')]
base_url = 'http://www.ssense.com/en-ca/men/designers/'

class SsenseSpider(scrapy.Spider):
	name = "ssense"
	# start_urls = [client.scrapyGet(url=f'http://www.ssense.com/en-ca/men/designers/{brandName}/{category}') for category in categories for brandName in brandNames]

	def start_requests(self):
		for brandName in brandNames:
			print(f'SCRAPING {brandName}')
			for category in categories:
				print(f'	SCRAPING {category}')
				data = {'brandName': brandName, 'category': category}
				yield scrapy.Request(client.scrapyGet(url=f'http://www.ssense.com/en-ca/men/designers/{brandName}/{category}'), meta=data)


	def parse(self, response):
		# links = response.xpath("//img/@data-srcset")
		brand_name = response.meta['brandName']
		category_name = response.meta['category']
		print(brand_name, category_name)
		currURL = response.request.url
		#category = currURL.split('/')[-1]
		print(currURL, currURL.split('/'))

		SSENSE_LINK = "http://www.ssense.com/en-ca"
		
		#brand_name = response.xpath("//h1[@id='listing-title']/text()").extract()
		# if(brand_name):
		# 	brand_name = brand_name[0] 

		product_script = response.xpath("//figure[@class='browsing-product-item']/script/text()").extract()
		# print(product_script)
		product_json = [json.loads(ps.replace("\n", "")) for ps in product_script]
		# print(product_json)



		brand, brand_created = Brand.objects.get_or_create(name=brand_name)
		brand.save()

		ssense_site, site_created = Site.objects.get_or_create(name="Ssense", link=SSENSE_LINK)
		ssense_site.save()

		print("category:", category_name)
		print(map_category(category_name))
		category, category_created = Category.objects.get_or_create(name=map_category(category_name))
		category.save()

		for itemJson in product_json:
			product_ID = itemJson["productID"]
			product_SKU = itemJson["sku"]
			product_name = itemJson["name"]
			product_price = itemJson["offers"]["price"]
			product_currency = itemJson["offers"]["priceCurrency"]
			product_url = itemJson["url"]
			product_image = itemJson["image"]
			product_avail = itemJson["offers"]["availability"]
			if(product_url.split("/")[1].lower() == "men"):
				gender = "M"
			elif(product_url.split("/")[1].lower() == "women"):
				gender = "F"
			else:
				gender = "U"



			# print(len(str(product_ID)), 
			# 	len(str(product_SKU)), 
			# 	len(str(product_name)), 
			# 	len(str(product_price)), 
			# 	len(str(product_currency)), 
			# 	len(str(product_url)), 
			# 	len(str(product_image)), 
			# 	len(str(product_avail)),
			# 	len(brand.name),
			# 	len(gender),
			# 	len(category))


			p, created = Product.objects.update_or_create(
				product_name=product_name,
				web_specific_id=product_ID,
				defaults={
					'sale_price': product_price,
					'currency': product_currency,
					'brand': brand, 
					'associated_site': ssense_site,
					'product_link': product_url, 
					'product_image': product_image,
					'gender': gender,
					'category': category,	
				}
			)
			p.save()
			if(created):
				print("created")	

			product_history_item, ph_created = PriceHistory.objects.update_or_create(
				product=p, 
				date=datetime.date.today(),
				currency=product_currency,
				defaults={
					'price': product_price,
				}
			)
			product_history_item.save()

			# yield scrapy.Request(
			# 	client.scrapyGet(url=(SSENSE_LINK + product_url)),
			# 	callback=self.parse_product,
			# 	meta={'product': p}
			# )

		#bName = brand_name.strip().lower().replace(" ", "-")

		pageExtract = response.xpath("//li/a[contains(text(), '→')]/@href").extract()
		nextPage = None
		if(pageExtract):
			nextPage = pageExtract[0][-1]

		if(nextPage):
			meta_data = {'brandName': brand_name, 'category': category_name}
			yield scrapy.Request(client.scrapyGet(url=f'http://www.ssense.com/en-ca/men/designers/{brand_name}/{category_name}?page={nextPage}'), meta=meta_data, callback=self.parse)


	# TODO: parse products when things are more stable
	def parse_product(self, response):
		# print("response!! :", response, response.body)
		product = response.meta['product']
		oneSize = response.xpath("//div[contains(@class, 'onesize')]/text()").extract()
		print(oneSize)

		if(multiSizeText):
			sizes = [size.strip() for size in multiSizeText[1:]]
		else:
			sizes = oneSize

		product_stock_item, ps_created = ProductStock.objects.update_or_create(
			product=product,
			defaults={
				'stock_data': sizes
			}
		)
		product_stock_item.save()

		print(product_stock_item)
		print(sizes)
