# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ProductItem(Item):
    url = Field()
    category_id = Field()
    category_name = Field()
    product_id = Field()
    product_name = Field()
    product_vendor_id = Field()
    product_vendor_name = Field()
    product_description = Field()
    product_price_now = Field()
    product_price_old = Field()
    product_currency = Field()
    product_weight_kg = Field()
    product_size_mm = Field()
    product_photo_urls = Field()
    product_photo_down = Field()
    product_properties = Field()
    product_available = Field()
