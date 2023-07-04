import scrapy
from frikibot.items import BoardGameItem


class EntreJuegosSpider(scrapy.Spider):
    name = "entrejuegos"
    allowed_domains = ["entrejuegos.cl"]

    def start_requests(self):
        start_url = "https://www.entrejuegos.cl/1064-juegos-de-mesa"
        yield scrapy.Request(url=start_url, callback=self.discover_product_urls)

    def discover_product_urls(self, response):
        xpath_selector = "//a[@class='thumbnail product-thumbnail']/@href"
        products_url = response.xpath(xpath_selector).getall()
        for url in products_url:
            yield scrapy.Request(url=url, callback=self.parse_product_data)

    def parse_product_data(self, response):
        product_item = BoardGameItem()
        product_item["name"] = response.xpath("//div[@class='col-md-6']/h1/text()").get()
        product_item["price"] = response.xpath("//span[@class='current-price-value']/@content").get()
        product_item["stock"]: response.xpath("//div[@class='product-quantities']/span/@data-stock").get()
        product_item["url"]: response.url
        yield product_item
