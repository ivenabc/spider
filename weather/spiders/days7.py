# -*- coding: utf-8 -*-
import scrapy
from utils.user_agent import get_random_useragent
from weather.items import MainLoader, WeatherItem, TodayItem, TodayLoader
import logging
import time

class Days7Spider(scrapy.Spider):
    name = 'days7'
    allowed_domains = ['weather.com.cn']

    def start_requests(self):
        url = 'http://www.weather.com.cn/weather/101221501.shtml'
        headers = {
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": 1,
            "User-Agent": get_random_useragent(), 
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        options = response.css('ul.t.clearfix > li')
        for index,option in enumerate(options):
            loader = MainLoader(item=WeatherItem(), selector=option, response=response)
            loader.add_css('title', 'li>.wea::text')
            loader.add_css('weather', 'li>.wea::text')
            loader.add_css('max_temprature', 'li > .tem span::text')
            loader.add_css('min_temprature', 'li > .tem i::text')
            loader.add_css('wind','li.sky .win em span::attr(title)')
            loader.add_css('wind_summary', 'li .win i::text')
            loader.add_value('index', index)
            yield loader.load_item()