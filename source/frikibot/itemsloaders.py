from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
import re


def transform_single_quote(text):
    return text.replace("'", "''")


def remove_newline_character(text):
    return text.replace("\n", "")


def remove_multiple_whitespaces(text):
    return re.sub(" {2,}", " ", text)


def remove_leading_and_trailing_spaces(text):
    return text.strip()


class BoardGameLoader(ItemLoader):

    default_output_processor = TakeFirst()

    product_availability_in = MapCompose(
        remove_newline_character,
        remove_multiple_whitespaces,
        remove_leading_and_trailing_spaces
    )

    # product_name_in = MapCompose(
    #    transform_single_quote
    # )
