# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
import json


class UtkonosPipeline(object):
    def process_item(self, item, spider):
        return item


class SqlitePipeline(object):

    collection_name = 'items'

    def __init__(self, sqlite_file):
        self.sqlite_file = sqlite_file

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sqlite_file = crawler.settings.get("SQLITE_FILE")
        )

    def open_spider(self, spider):
        self.db_conn = sqlite3.connect(self.sqlite_file)
        c = self.db_conn.cursor()
        c.executescript(
        '''
        create table if not exists items (
            url primary key,
            cat_id,
            item_id,
            vendor_id,
            name,
            category,
            weight,
            size,
            description,
            photo_urls,
            photo_down,
            properties,
            price_cur,
            price_old,
            min_amount,
            available
        );
        '''
        )

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()

    def process_item(self, item, spider):
        c = self.db_conn.cursor()
        c.execute(
        '''
        insert or replace into items(
            url,
            cat_id,
            item_id,
            vendor_id,
            name,
            category,
            weight,
            size,
            description,
            photo_urls,
            photo_down,
            properties,
            price_cur,
            price_old,
            min_amount,
            available
        ) values (
            :url,
            :cat_id,
            :item_id,
            :vendor_id,
            :name,
            :category,
            :weight,
            :size,
            :description,
            :photo_urls,
            :photo_down,
            :properties,
            :price_cur,
            :price_old,
            :min_amount,
            :available
        );
        '''
        ,
        {
            'url': item['url'],
            'cat_id': item['cat_id'],
            'item_id': item['item_id'],
            'vendor_id': item.get('vendor_id', ''),
            'name': item.get('name', ''),
            'category': item.get('category', ''),
            'weight': item.get('weight', ''),
            'size': item.get('size', ''),
            'description': item.get('description', ''),
            'photo_urls': json.dumps(item.get('photo_urls', '')),
            'photo_down': json.dumps(item.get('photo_down', '')),
            'properties': json.dumps(item.get('properties', ''), ensure_ascii=False),
            'price_cur': item.get('price_cur', ''),
            'price_old': item.get('price_old', ''),
            'min_amount': item.get('min_amount', ''),
            'available': item.get('available', '')
        }
        )
        self.db_conn.commit()
        return item
