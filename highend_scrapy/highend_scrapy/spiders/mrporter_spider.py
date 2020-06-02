import scrapy
from scrapy.http.request import Request
from highend_scrapy.items import ProductItem, BrandItem, SiteItem
from main.models import Product, Brand, Site

brandNames = [line.rstrip() for line in open('../lib/brand_names.txt')]

class MrporterSpider(scrapy.Spider):
	name = "mrporter"
	start_urls = [f'https://www.mrporter.com/en-ca/mens/designer/{brandNameItem}' for brandNameItem in brandNames]
	# https://www.ssense.com/en-ca/men/designers/acne-studios?page=7
	# loop through till the last page

	def start_requests(self):
		# headers= {'User-Agent': 'IBM WebExplorer /v0.94'}
		for url in self.start_urls:
			print(url)
			yield Request(url)

	def parse(self, response):
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


