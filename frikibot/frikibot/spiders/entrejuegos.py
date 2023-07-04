import scrapy


class EntreJuegosSpider(scrapy.Spider):
    name = "entrejuegos"
    allowed_domains = ["entrejuegos.cl"]
    start_urls = ["https://www.entrejuegos.cl/1064-juegos-de-mesa"]

    def start_request(self):
        yield scrapy.Request(url=self.start_urls, callback=self.discover_product_urls)

    def discover_product_urls(self, response):
        xpath_selector = "//a[@class='thumbnail product-thumbnail']/@href"
        products_url = response.css(xpath_selector).getall()
        for url in products_url:
            yield scrapy.Request(url=url, callback=self.parse_product_data)

    def parse_product_data(self, response):

        yield {
            "name": response.xpath("//div[@class='col-md-6']/h1/text()").get(),
            "price": response.xpath("//span[@class='current-price-value']/@content").get(),
            "stock": response.xpath("//div[@class='product-quantities']/span/@data-stock").get(),
            "url": '',
            "product_id": response.xpath("//div[@class='product-reference']/span/text()").get(),
        }

