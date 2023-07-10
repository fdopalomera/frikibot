import scrapy
from datetime import datetime
from source.frikibot.items import BoardGameItem
from source.frikibot.itemsloaders import BoardGameLoader


class EntreJuegosSpider(scrapy.Spider):
    name = "entrejuegos"
    allowed_domains = ["entrejuegos.cl"]

    def start_requests(self):
        start_url = "https://www.entrejuegos.cl/1064-juegos-de-mesa"
        yield scrapy.Request(url=start_url, callback=self.discover_product_urls)

    def discover_product_urls(self, response):
        xpath_selector = "//a[@class='thumbnail product-thumbnail']/@href"
        products_url = response.xpath(xpath_selector).getall()
        meta = {
            "scraping_started_at": datetime.now()
        }
        for url in products_url:
            yield scrapy.Request(url=url, callback=self.parse_product_data, meta=meta)



    def parse_product_data(self, response):

        loader = BoardGameLoader()
        loader.add_xpath("product_name", "//div[@class='col-md-6']/h1/text()")
        loader.add_xpath("product_price", "//span[@class='current-price-value']/@content")
        loader.add_xpath("product_stock", "//div[@class='product-quantities']/span/@data-stock")
        loader.add_value("product_url", response.url)
        loader.add_value("scraped_at", response.meta["scraping_started_at"])
        loader.add_xpath("product_id", "//div[@class='product-reference']/span/text()")
        loader.add_xpath("product_condition", "//div[@class='product-condition']/span/text()")
        #loader.add_value("store_name", self.name)
        yield loader
