# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class ShopItem(Item):
    url = Field()
    cat_id = Field()
    item_id = Field()
    vendor_id = Field()
    name = Field()
    category = Field()
    weight = Field()
    size = Field()
    description = Field()
    photo_urls = Field()
    photo_down = Field()
    properties = Field()
    price_cur = Field()
    price_old = Field()
    min_amount = Field()
    available = Field()
