import random
import csv
import json
import urllib

import scrapy
from scrapy_redis.spiders import RedisSpider

from stock_all.items import StockInfoItem


class StockInfo(RedisSpider):
    name = 'stock_info'
    unstock = open('unstock.txt', 'w')
    redis_key = "stock_info:start_urls"
    custom_settings = {
        'ITEM_PIPELINES': {'scrapy_redis.pipelines.RedisPipeline': 300,
                           'stock_all.pipelines.'}
    }

    def make_requests_from_url(self, url):
        headers = {
            'Host': 'xueqiu.com',
        }
        return scrapy.Request(url, headers=headers, meta={'cookiejar':1})

    def parse(self, response):
        cookies = response.headers.getlist(b'Set-Cookie')
        print(cookies)
        with open('companys.csv', 'r', encoding='gbk') as f:
            comps = list(csv.reader(f))
        for comp in comps:
            url = r'https://xueqiu.com/stock/search.json'
            referer = r'https://xueqiu.com/k?q=' + comp[0]
            headers = {
                'Host': 'xueqiu.com',
                'Referer': referer,
            }
            params = {
                'code': comp
            }
            yield scrapy.FormRequest(url, headers=headers,formdata=params,
                                      meta={'cookiejar':response.meta['cookiejar']}, callback=self.parse1)

    def parse1(self, response):
        info = StockInfoItem()
        try:
            stocks = json.loads(response.text)['stocks'][0]
            info['code'] = stocks['code']
            info['ind_id'] = stocks['ind_id']
            info['ind_name'] = stocks['ind_name']
            info['name'] = stocks['name']
            info['stock_id'] = stocks['stock_id']
            info['stock_type'] = stocks['type']
            yield info
        except IndexError as e:
            stock = urllib.parse.unquote(response.request.body.decode('utf-8').split('=')[1])
            print('<{0}>,未查询到上市信息!'.format(stock))
            self.unstock.write(stock+'\n')