# -*- coding: utf-8 -*-

import re

from scrapy.spiders import SitemapSpider

from utkonos.items import ShopItem


class CollectorSpider(SitemapSpider):
    name = "collector"
    allowed_domains = ["utkonos.ru"]
    sitemap_urls = ['http://www.utkonos.ru/images/sitemap/sitemap_index.xml']
    sitemap_rules = [('/item/', 'parse_item')]

    def parse(self, response):
        pass

    def parse_item(self, response):

        item = ShopItem()

        item['url'] = response.url

        m = re.search('/item/(\d+)/(\d+)', response.url)

        if m:
            item['cat_id'], item['item_id'] = m.groups()

        vendor_id = ' '.join(
            response.css('div.item_menu_hash span::text').extract()
        )

        if vendor_id:
            m = re.search('\W+:\s+(\d+)', vendor_id)
            if m:
                item['vendor_id'] = m.group(1)

        item['name'] = ' '.join(
            response.css('h1.goods_view_item-header::text').extract()
        )

        item['weight'] = ' '.join(
            response.css('div.goods_item_sale_unit b::text').extract()
        )

        item['size'] = ' '.join(
            response.css('div.goods_item_size b::text').extract()
        )

        item['description'] = ' '.join(
            response.css('.page_item_description div').extract()
        )

        item['properties'] = []
        props = response.css('div.goods_item_properties div')

        for p in props:
            key = ' '.join(p.css('div span span::text').extract())
            val = ' '.join(p.css('div a::text').extract())
            item['properties'].append({key: val})

        item['price_cur'] = ' '.join(
            response.css('div.goods_price-item.current::text').extract()
        )

        item['price_old'] = ' '.join(
            response.css('div.goods_price-item.old span::text').extract()
        )

        if response.css('span.not_stock'):
            item['available'] = False
        else:
            item['available'] = True

        item['photo_urls'] = []

        for img in response.css('.goods_pic > a::attr("data-pic-high")').extract():
            item['photo_urls'].append(response.urljoin(re.sub('\?\d+$', '', img)))

        yield item
