# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymysql

from Utils.mysql_api import MysqlConn, MysqlOpt

logging.basicConfig(level=logging.INFO)


class BasePipeline(object):
    """pipeline基类，用于访问settings参数,连接数据库，提供连接表方法"""
    def __init__(self, host, port, user, password, database):
        self.conn_db = MysqlConn(
            host=host, port=port, user=user, password=password, database=database)
        logging.info((host, port, user, password, database))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            port=crawler.settings.get('MYSQL_PORT'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            database=crawler.settings.get('MYSQL_DB')
        )

    def connect_tb(self, tbname):
        conn_tb = MysqlOpt(self.conn_db, tbname)
        return conn_tb


class StockInfoPipeline(BasePipeline):
    """连接info表，将item分析后存入表中"""
    def open_spider(self, spider):
        self.conn_tb_info = self.connect_tb('info')

    def close_spider(self, spider):
        self.conn_db.close()

    def process_item(self, item, spider):
        try:
            #print(item.values)
            self.conn_tb_info.insert(list(item.values()))
            return item
        except pymysql.err.IntegrityError as e:
            logging.info('<'+item['name']+'>'+'该公司信息已存在!')


class StockBaseLinksPipeline(BasePipeline):
    """
    创建info表连接，并赋给spider，使得可在spider中使用该连接获取数据,
    创建base_links表连接，分析item后，存入数据库中
    """
    def open_spider(self, spider):
        self.conn_tb_info = self.connect_tb('info')
        self.conn_tb_links = self.connect_tb('base_links')
        spider.conn_tb_info = self.conn_tb_info

    def close_spider(self, spider):
        self.conn_db.close()

    def process_item(self, item, spider):
        link = item['links']
        self.conn_tb_links.insert(link)
        return item

class DataPipeline(BasePipeline):
    """
    创建表links连接，传递给spider
    """
    def open_spider(self, spider):
        spider.conn_tb_links = self.connect_tb('base_links')
        spider.conn_tb_gsjj = self.connect_tb('gsjj')
        spider.conn_tb_zycwzb = self.connect_tb('zycwzb')

    def close_spider(self, spider):
        self.conn_db.close()

    def process_item(self, item, spider):
        return item
