from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose


def remove_thousands_separator(text):
    return text.replace('.', '')


def remove_price_sign(text):
    return text.replace('$', '')


class BoardGameLoader(ItemLoader):

    default_output_processor = TakeFirst()
    price_in = MapCompose(remove_price_sign, remove_thousands_separator)
