# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
import json

from utkonos.items import ProductItem


DEFAULT_SQLITE_FILE = 'output.db'
DEFAULT_COMMIT_WATERMARK = 100


class UtkonosPipeline(object):
    def process_item(self, item, spider):
        return item


class SqlitePipeline(object):

    collection_name = 'products'
    commit_watermark = DEFAULT_COMMIT_WATERMARK  # Commit after so many items
    commit_items_cnt = 0

    def __init__(self,
                 sqlite_file=DEFAULT_SQLITE_FILE,
                 commit_watermark=DEFAULT_COMMIT_WATERMARK):
        self.sqlite_file = sqlite_file
        self.commit_watermark = commit_watermark

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sqlite_file=crawler.settings.get("SQLITE_FILE",
                                             DEFAULT_SQLITE_FILE),
            commit_watermark=crawler.settings.get("SQLITE_COMMIT_WATERMARK",
                                                  DEFAULT_COMMIT_WATERMARK)
        )

    def open_spider(self, spider):
        self.db_conn = sqlite3.connect(self.sqlite_file)
        # self.db_conn.isolation_level = None
        cur = self.db_conn.cursor()
        qry = 'create table if not exists %s (%s, primary key (url));' % \
            (self.collection_name, ', '.join(ProductItem.fields),)
        cur.executescript(qry)

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()

    def process_item(self, item, spider):

        cur = self.db_conn.cursor()

        product = dict(item)

        for k in product:
            if k == 'product_photo_urls' or k == 'product_photo_down':
                product[k] = json.dumps(product[k])
            elif k == 'product_properties':
                product[k] = json.dumps(product[k], ensure_ascii=False)

        qry = 'insert or replace into %s (%s) values (%s);' % (
            self.collection_name,
            ', '.join(product.keys()),
            ':' + ', :'.join(product.keys())
        )

        cur.execute(qry, product)
        self.commit_items_cnt += 1

        if self.commit_items_cnt >= self.commit_watermark:
            self.db_conn.commit()
            self.commit_items_cnt = 0

        return item
