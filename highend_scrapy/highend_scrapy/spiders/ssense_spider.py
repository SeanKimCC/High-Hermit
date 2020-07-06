import scrapy
from scrapy.http.request import Request
from highend_scrapy.items import ProductItem, BrandItem, SiteItem, PriceHistoryItem, ProductStockItem
from main.models import Product, Brand, Site, PriceHistory, ProductStock
from random import randint
from scraper_api import ScraperAPIClient
import datetime
import json

client = ScraperAPIClient('f73c58f148ce7452a6a188078c7888e5')

brandNames = [line.rstrip() for line in open('../resrc/brand_names.txt')]
randUAs = [line.rstrip() for line in open('../resrc/rand_user_agents.txt')]

class SsenseSpider(scrapy.Spider):
	name = "ssense"
	# start_urls = [f'https://www.ssense.com/en-ca/men/designers/{brandName}' for brandName in brandNames]
	start_urls = [client.scrapyGet(url=f'http://www.ssense.com/en-ca/men/designers/{brandName}') for brandName in brandNames]
	#client.scrapyGet(url = 'http://httpbin.org/ip')
	# start_urls = [f'https://www.ssense.com/en-ca/men/designers/acne-studios']
	# https://www.ssense.com/en-ca/men/designers/acne-studios?page=7
	# loop through till the last page

	# def start_requests(self):
	# 	# randUA = randUAs[randint(0, len(randUAs) - 1)]
	# 	# headers= {'User-Agent': f'{randUA}'}
	# 	# headers = {'User-Agent': 'Enigma Browser'}
	# 	for url in self.start_urls:
	# 		# print(url)
	# 		# # yield Request(url, meta={'ua': 'desktop'})
	# 		yield Request(url)

	def parse(self, response):
		# links = response.xpath("//img/@data-srcset")
		SSENSE_LINK = "http://www.ssense.com/en-ca"
		pageExtract = response.xpath("//li/a[contains(text(), '→')]/@href").extract()
		nextPage = None
		if(pageExtract):
			nextPage = pageExtract[0][-1]
		brand_name = response.xpath("//h1[@id='listing-title']/text()").extract()
		if(brand_name):
			brand_name = brand_name[0] 

		product_script = response.xpath("//figure[@class='browsing-product-item']/script/text()").extract()
		# print(product_script)
		product_json = [json.loads(ps.replace("\n", "")) for ps in product_script]
		# print(product_json)



		brand, brand_created = Brand.objects.get_or_create(name=brand_name)
		brand.save()

		ssense_site, site_created = Site.objects.get_or_create(name="Ssense", link=SSENSE_LINK)
		ssense_site.save()

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

			yield scrapy.Request(
				client.scrapyGet(url=(SSENSE_LINK + product_url)),
				callback=self.parse_product,
				meta={'product': p}
			)

		bName = brand_name.strip().lower().replace(" ", "-")
		url = response.request.url
		if(nextPage):
			# randUA = randUAs[randint(0, len(randUAs) - 1)]
			# yield Request(f'https://www.ssense.com/en-ca/men/designers/{bName}?page={nextPage}', headers={'User-Agent': f'{randUA}'})
			yield scrapy.Request(client.scrapyGet(url=f'http://www.ssense.com/en-ca/men/designers/{bName}?page={nextPage}'), callback=self.parse)

	def parse_product(self, response):
		# print("response!! :", response, response.body)
		product = response.meta['product']
		multiSizeText = response.xpath("//select[@id='size']/option/text()").extract()
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
