import scrapy
from scrapy.http.request import Request
from highend_scrapy.items import ProductItem, BrandItem, SiteItem, PriceHistoryItem, ProductStockItem
from main.models.models import Product, Brand, Site, PriceHistory, ProductStock
from main.models.CategoryModel import Category
from random import randint
from scraper_api import ScraperAPIClient
import datetime
import json

client = ScraperAPIClient('fb2e3bc1b5fcb297e8b83a4aa703d199')

brandNames = [line.rstrip() for line in open('../resrc/brand_names.txt')]
randUAs = [line.rstrip() for line in open('../resrc/rand_user_agents.txt')]
categories = [line.rstrip() for line in open('../resrc/categories/mrporter-categories.txt')]
base_url = 'http://www.ssense.com/en-ca/men/designers/'

class MrporterSpider(scrapy.Spider):
	name = "mrporter"
	start_urls = [f'https://www.mrporter.com/en-ca/mens/designer/{brandNameItem}' for brandNameItem in brandNames]
	# https://www.ssense.com/en-ca/men/designers/acne-studios?page=7
	# loop through till the last page

	def start_requests(self):
		# headers= {'User-Agent': 'IBM WebExplorer /v0.94'}
		category_set = {
			'clothing': ['blazers', 'casual-shirts', 'coats-and-jackets', 'jeans', \
			'knitwear', 'pants', 'polo-shirts', 'shorts', 'suits', 'sweats', 'swimwear', 't-shirts'],
			'shoes': ['boots', 'sneakers', 'derby-shoes', 'loafers', 'sandals', 'slides', 'slippers'],
			'accessories': ['bags', 'hats', 'scarves', 'wallets']
		}
		for brandName in brandNames:
			print(f'SCRAPING {brandName}')
			for category in categories:
				print(f'	SCRAPING {category}')
				for sub_category in category_set[category]:
					print(f'		SCRAPING {sub_category}')
					data = {'brandName': brandName, 'category': category}
					yield scrapy.Request(client.scrapyGet(url=f'http://www.ssense.com/en-ca/men/designers/{brandName}/{category}'), meta=data)

		for brandName in brandNames:
			print(f'SCRAPING {brandName}')
			for category in categories:
				print(f'	SCRAPING {category}')
				data = {'brandName': brandName, 'category': category}
				yield scrapy.Request(client.scrapyGet(url=f'http://www.ssense.com/en-ca/men/designers/{brandName}/{category}'), meta=data)


	def parse(self, response):

		brand_name = response.meta['brandName']
		category_name = response.meta['category']
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

		category, category_created = Category.objects.get_or_create(name=category_name.upper())
		category.save()
		
		# links = response.xpath("//img/@data-srcset")
		pageCounter = response.xpath("//span[@class='Pagination6__currentPage']/text()").extract()[0].split()
		print(pageCounter)
		currPage = int(pageCounter[-3])
		numPages = int(pageCounter[-1])

		product_prices = response.xpath("//span[@itemprop='price']/text()").extract()
		product_names = response.xpath("//span[@class='ProductItem23__name']/text()").extract()
		brandName = response.xpath("//h1[@class='Header5__title']/text()").extract()
		if(brandName):
			brandName = brandName[0]

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

		acne_brand, brand_created = Brand.objects.get_or_create(name=brandName)
		acne_brand.save()

		mrporter_site, site_created = Site.objects.get_or_create(name="MrPorter", link="https://www.mrporter.com/")
		mrporter_site.save()
		# print(Brand.objects.all())



		for i in range(loopLen):
			p, created = Product.objects.update_or_create(product_name=product_names[i], 
				defaults={'sale_price': product_prices[i],\
				'brand': acne_brand, 'associated_site': mrporter_site})
			print(p)

			if(created):
				print("created")
			# p = Product.objects.update_or_create(product_name=product_names[i], sale_price=product_prices[i],\
			# 	brand=acne_brand, associated_site=ssense_site)
			p.save()


		if(numPages > currPage):
			currPage += 1
			yield Request(f'https://www.mrporter.com/en-ca/mens/designer/acne-studios?pageNumber={currPage}')


