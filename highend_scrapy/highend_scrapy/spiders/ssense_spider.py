import scrapy
from scrapy.http.request import Request
from highend_scrapy.items import ProductItem, BrandItem, SiteItem
from main.models import Product, Brand, Site
from random import randint
from scraper_api import ScraperAPIClient

client = ScraperAPIClient('fd658098edb00dd7976ec39c9f8f32f3')

brandNames = [line.rstrip() for line in open('../lib/brand_names.txt')]
randUAs = [line.rstrip() for line in open('../lib/rand_user_agents.txt')]

class SsenseSpider(scrapy.Spider):
	name = "ssense"
	# start_urls = [f'https://www.ssense.com/en-ca/men/designers/{brandName}' for brandName in brandNames]
	start_urls = [client.scrapyGet(url=f'https://www.ssense.com/en-ca/men/designers/{brandName}') for brandName in brandNames]
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
		pageExtract = response.xpath("//li/a[contains(text(), '→')]/@href").extract()
		nextPage = None
		if(pageExtract):
			nextPage = pageExtract[0][-1]
		brand_name = response.xpath("//h1[@id='listing-title']/text()").extract()
		if(brand_name):
			brand_name = brand_name[0]
		product_prices = response.xpath("//span[@class='price']/text()").extract()
		product_names = response.xpath("//p[@class='product-name-plp']/text()").extract()


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
			print(product_names[i], product_prices[i])

		acne_brand, brand_created = Brand.objects.get_or_create(name=brand_name)
		acne_brand.save()

		ssense_site, site_created = Site.objects.get_or_create(name="Ssense", link="https://www.ssense.com/")
		ssense_site.save()
		# print(Brand.objects.all())



		for i in range(loopLen):
			p, created = Product.objects.update_or_create(product_name=product_names[i], 
				defaults={'sale_price': product_prices[i],\
				'brand': acne_brand, 'associated_site': ssense_site})

			if(created):
				print("created")
			# p = Product.objects.update_or_create(product_name=product_names[i], sale_price=product_prices[i],\
			# 	brand=acne_brand, associated_site=ssense_site)
			p.save()

		bName = brand_name.strip().lower().replace(" ", "-")
		if(nextPage):
			randUA = randUAs[randint(0, len(randUAs) - 1)]
			# yield Request(f'https://www.ssense.com/en-ca/men/designers/{bName}?page={nextPage}', headers={'User-Agent': f'{randUA}'})
			yield Request(client.scrapyGet(url=f'https://www.ssense.com/en-ca/men/designers/{bName}?page={nextPage}'))

