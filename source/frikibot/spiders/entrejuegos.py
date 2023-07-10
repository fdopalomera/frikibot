import scrapy
import pendulum
from frikibot.items import EntrejuegosItem
from frikibot.itemsloaders import EntrejuegosLoader


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
            "scraping_started_at": pendulum.now(tz="UTC")
        }
        for url in products_url:
            yield scrapy.Request(url=url, callback=self.parse_product_data, meta=meta)

        # Continue with the next page
        #next_page = response.xpath("//a[@class='next js-search-link']/@href").get()
        #if next_page is not None:
            #yield response.follow(next_page, callback=self.discover_product_urls)

    def parse_product_data(self, response):

        loader = EntrejuegosLoader(item=EntrejuegosItem(), response=response)
        loader.add_xpath("product_name", "//div[@class='col-md-6']/h1/text()")
        loader.add_xpath("product_price", "//span[@class='current-price-value']/@content")
        loader.add_value("product_url", response.url)
        loader.add_value("scraped_at", response.meta["scraping_started_at"])
        loader.add_xpath("product_id", "//div[@class='product-reference']/span/text()")

        qty_xpath = "//div[@class='product-quantities']/span/@data-stock"
        if not response.xpath(qty_xpath):
            loader.add_value("product_stock", 0)
        else:
            loader.add_xpath("product_stock", qty_xpath)

        yield loader.load_item()
