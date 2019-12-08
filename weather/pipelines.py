# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import json
from scrapy.utils.serialize import ScrapyJSONEncoder
import os
import psycopg2
from .items import City
# import sys
# sys.setdefaultencoding('utf-8')


class WeatherPipeline(object):
    def process_item(self, item, spider):
        # logging.warning(item)
        # logging.log(logging.WARNING, item)
        logging.warning("current_database:{}".format(os.getcwd()))
        return item


class JsonWriterPipeline(object):
    def open_spider(self, spider):
        self.file = open('items.jl', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        encoder = ScrapyJSONEncoder(ensure_ascii=False)
        line = encoder.encode(item)
        self.file.write(line)
        self.file.write(item['sun_up_at'])
        return item


class PostgresPipeline(object):
    def __init__(self):
        with open(os.getcwd() + "/postgres.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.config = data

    def open_spider(self, spider):
        self.client = psycopg2.connect(**self.config)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, City):
            logging.warning(item['province'])
            self.process_cities(item)
        else: 
            encoder = ScrapyJSONEncoder(ensure_ascii=False)
            line = encoder.encode(item)
            cur = self.client.cursor()
            cur.execute('INSERT INTO weather VALUES(now(),CURRENT_DATE,%s) ON CONFLICT(today_date) DO UPDATE SET updatedat=now(),information=%s', 
                (line, line))
            self.client.commit()
            cur.close()
        return item 
    
    def process_cities(self, item):
        if item['cityid'] == '0':
            return 
        cur = self.client.cursor()
        cur.execute('INSERT INTO weather_cities(province,cityid,cityname) VALUES(%s,%s,%s) ON CONFLICT(cityid) DO NOTHING;',
         (item['province'], item['cityid'], item['cityname']))
        self.client.commit()
        cur.close()
