from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose


def transform_single_quote(text):
    return text.replace("'", "''")


class EntrejuegosLoader(ItemLoader):

    default_output_processor = TakeFirst()
    product_name_in = MapCompose(transform_single_quote)
