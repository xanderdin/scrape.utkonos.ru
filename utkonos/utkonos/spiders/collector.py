# -*- coding: utf-8 -*-

import re
import html2text

from scrapy.spiders import SitemapSpider

from utkonos.items import ProductItem


class CollectorSpider(SitemapSpider):
    name = "collector"
    allowed_domains = ["utkonos.ru"]
    sitemap_urls = ['http://www.utkonos.ru/images/sitemap/sitemap_index.xml']
    sitemap_rules = [('/item/', 'parse_item')]

    def parse(self, response):
        pass

    def parse_item(self, response):

        item = ProductItem()

        item['url'] = response.url

        script = ''
        for s in response.css('script::text').extract():
            if ' dataLayer = ' in s:
                script = s
                break

        m = re.search('productCategoryName.*:.*"(.+)"', script)
        if m:
            item['category_name'] = m.group(1)

        m = re.search('productCategoryId.*:.*"(.+)"', script)
        if m:
            item['category_id'] = m.group(1)

        m = re.search('productAvailability.*:.*"(.+)"', script)
        if m and m.group(1) == 'available':
            item['product_available'] = True
        else:
            item['product_available'] = False

        m = re.search('productId.*:.*"(.+)"', script)
        if m:
            item['product_id'] = m.group(1)

        m = re.search('productName.*:.*"(.+)"', script)
        if m:
            item['product_name'] = m.group(1)

        m = re.search('productVendorName.*:.*"(.+)"', script)
        if m:
            item['product_vendor_name'] = m.group(1)

        m = re.search('productVendorId.*:.*"(.+)"', script)
        if m:
            item['product_vendor_id'] = m.group(1)

        m = re.search('productPriceLocal.*:.*"(.+)"', script)
        if m:
            try:
                item['product_price_now'] = float(m.group(1))
            except:
                pass

        m = re.search('productOldPriceLocal.*:.*"(.+)"', script)
        if m:
            try:
                item['product_price_old'] = float(m.group(1))
            except:
                pass

        m = re.search("'currencyCode\'.*:.*'(.+)'", script)
        if m:
            item['product_currency'] = m.group(1)

        item['product_weight_kg'] = re.sub('[^\d\.]+', '', ' '.join(
            response.css('div.goods_item_sale_unit b::text').extract()
        ))

        item['product_size_mm'] = re.sub('[^\d\xd7]+', '', ' '.join(
            response.css('div.goods_item_size b::text').extract()
        ))

        item['product_description'] = html2text.HTML2Text().handle(
            ' '.join(
                response.css('.page_item_description div').extract()
            )
        )

        item['product_properties'] = []
        props = response.css('div.goods_item_properties div')

        for p in props:
            key = ' '.join(p.css('div span span::text').extract())
            val = ' '.join(p.css('div a::text').extract())
            item['product_properties'].append({key: val})

        item['product_photo_urls'] = []

        pics = response.css('.goods_pic > a::attr("data-pic-high")').extract()

        for img in pics:
            item['product_photo_urls'].append(
                response.urljoin(re.sub('\?\d+$', '', img))
            )

        yield item
