import scrapy
import pendulum
from frikibot.items import BoardGameItem
from frikibot.itemsloaders import BoardGameLoader


class MovieplaySpider(scrapy.Spider):
    name = "movieplay"
    allowed_domains = ["movieplay.cl"]
    start_url = "https://movieplay.cl/123-familiares.html"

    def start_requests(self):
        yield scrapy.Request(self.start_url, callback=self.discover_product_urls)

    def discover_product_urls(self, response):

        if response.status == 200:
            xpath_selector = "//a[@class='thumbnail product-thumbnail']/@href"
            products_url = response.xpath(xpath_selector).getall()
            meta = {
                "scraping_started_at": pendulum.now(tz="UTC")
            }
            for url in products_url:
                yield scrapy.Request(url, callback=self.parse_product_data, meta=meta)

            # Continue with the next page
            if response.url == self.start_url:
                next_page = "https://movieplay.cl/123-familiares.html?page=2"
            else:
                next_num = str(int(response.url[-1]) + 1)
                next_page = response.url[:-1] + next_num
            meta = {
                "dont_redirect": True,
                "handle_httpstatus_list": [302]
            }
            yield scrapy.Request(url=next_page, callback=self.discover_product_urls, meta=meta)

    def parse_product_data(self, response):
        loader = BoardGameLoader(item=BoardGameItem(), response=response)
        loader.add_xpath("product_name", "//h1[@itemprop='name']/span/text()")
        loader.add_xpath("product_price", "//span[@itemprop='price']/@content")
        loader.add_value("product_url", response.url)
        loader.add_value("scraped_at", response.meta["scraping_started_at"])
        loader.add_xpath("product_availability", "//span[@id='product-availability']/text()[2]")
        loader.add_xpath("product_sku", "//span[@itemprop='sku']/text()")

        return loader.load_item()
