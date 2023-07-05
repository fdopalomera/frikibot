import scrapy
import datetime
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
            "scraping_started_at": datetime.datetime.now()
        }
        for url in products_url:
            yield scrapy.Request(url=url, callback=self.parse_product_data, meta=meta)

    def parse_product_data(self, response):

        loader = BoardGameLoader()
        loader.add_xpath("name", "//div[@class='col-md-6']/h1/text()")
        loader.add_xpath("price", "//span[@class='current-price-value']/@content")
        loader.add_xpath("stock", "//div[@class='product-quantities']/span/@data-stock")
        loader.add_value("url", response.url)
        loader.add_value("scraped_at", response.meta["scraping_started_at"])
        loader.add_value("store", self.name)
        yield loader
