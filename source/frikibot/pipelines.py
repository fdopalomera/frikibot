# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector
from scrapy.exceptions import DropItem


class ExportToMySQLPipeline:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            host=settings.get('MYSQL_DATABASE_HOST'),
            user=settings.get('MYSQL_USER'),
            password=settings.get('MYSQL_PASSWORD'),
            database=settings.get('MYSQL_DATABASE')
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
        table_name = f"staging_{spider.name}_catalog"
        columns = ", ".join([key for key in item.keys()])
        values = "'" + "', '".join([str(value) for value in item.values()]) + "'"

        insert_query = f"""
        INSERT INTO {table_name}
        ({columns})
        VALUES
        ({values})
        """

        try:
            self.cursor.execute(insert_query)
            self.conn.commit()
        except mysql.connector.Error as e:
            raise DropItem(f"Error inserting item: {e}")
