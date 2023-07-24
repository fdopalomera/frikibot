import scrapy
import pendulum
from frikibot.items import BoardGameItem
from frikibot.itemsloaders import BoardGameLoader


class EntreJuegosSpider(scrapy.Spider):
    name = "entrejuegos"
    allowed_domains = ["entrejuegos.cl"]
    date = pendulum.today(tz="UTC").date()

    def start_requests(self):
        start_url = "https://www.entrejuegos.cl/1064-juegos-de-mesa"
        yield scrapy.Request(url=start_url, callback=self.discover_product_urls)

    def discover_product_urls(self, response):
        xpath_selector = "//a[@class='thumbnail product-thumbnail']/@href"
        products_url = response.xpath(xpath_selector).getall()
        meta = {
            "scraping_started_at": pendulum.now(tz="UTC")
        }
        for url in products_url:
            yield scrapy.Request(url=url, callback=self.parse_product_data, meta=meta)

        # Continue with the next page
        next_page = response.xpath("//a[@class='next js-search-link']/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.discover_product_urls)

    def parse_product_data(self, response):

        loader = BoardGameLoader(item=BoardGameItem(), response=response)
        loader.add_xpath("product_name", "//div[@class='col-md-6']/h1/text()")
        loader.add_xpath("product_price", "//span[@class='current-price-value']/@content")
        loader.add_value("product_url", response.url)
        loader.add_value("scraped_at", response.meta["scraping_started_at"])
        loader.add_xpath("product_reference", "//div[@class='product-reference']/span/text()")
        loader.add_value("store_name", self.name.title())

        qty_xpath = "//div[@class='product-quantities']/span/@data-stock"
        if not response.xpath(qty_xpath):
            loader.add_value("product_stock", 0)
        else:
            loader.add_xpath("product_stock", qty_xpath)

        yield loader.load_item()
