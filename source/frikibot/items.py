# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EntrejuegosItem(scrapy.Item):
    product_name = scrapy.Field()
    product_price = scrapy.Field()
    product_stock = scrapy.Field()
    product_url = scrapy.Field()
    scraped_at = scrapy.Field()
    product_id = scrapy.Field()

