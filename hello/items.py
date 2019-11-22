# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Identity

class HelloItem(Item):
    text = Field()
    tags = Field()
    author = Field()


class MainLoader(ItemLoader):
    default_output_processor  = TakeFirst()

    tags_out = Identity()


# default_headers = {
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#         'Accept-Encoding': 'gzip, deflate, sdch, br',
#         'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
#         'Cache-Control': 'max-age=0',
#         'Connection': 'keep-alive',
#         'Host': 'www.douban.com',
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
#     }