# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector
from scrapy.exceptions import DropItem


class ExportToMySQLPipeline:
    def __init__(self, host, user, password, database, table):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.table = table

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            host=settings.get('MYSQL_DATABASE_HOST'),
            user=settings.get('MYSQL_USER'),
            password=settings.get('MYSQL_PASSWORD'),
            database=settings.get('MYSQL_DATABASE'),
            table=settings.get('MYSQL_TABLE')
        )

    def open_spider(self, spider):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(f"""
                INSERT INTO {self.table}
                (scraped_at, product_name, product_price, product_stock, product_url, product_id, product_condition)
                VALUES 
                ({item['scraped_at']}, {item['product_name']}, {item['product_price']}, {item['product_stock']}, 
                    {item['product_url']}, {item['product_id']}, {item['product_condition']})
                """)  # TODO: Refactor with iteration through modeled items
            self.conn.commit()
        except mysql.connector.Error as e:
            raise DropItem(f"Error inserting item: {e}")
