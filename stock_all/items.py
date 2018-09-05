# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StockInfoItem(scrapy.Item):
    code = scrapy.Field()
    ind_id = scrapy.Field()
    ind_name = scrapy.Field()
    name = scrapy.Field()
    stock_id = scrapy.Field()
    stock_type = scrapy.Field()


class StockBasicLinksItem(scrapy.Item):
    links = scrapy.Field()


class GsjjItem(scrapy.Item):
    datas = scrapy.Field()


