# -*- coding: utf-8 -*-
import scrapy
import time
from utils.user_agent import get_random_useragent
from weather.items import MainLoader, WeatherItem, TodayItem, TodayLoader
import logging

class TodaySpider(scrapy.Spider):
    name = 'today'
    allowed_domains = ['weather.com.cn']

    def start_requests(self):
        url = 'http://www.weather.com.cn/weather1d/101221501.shtml'
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
        day = MainLoader(item=WeatherItem(), response=response)
        day.add_css('title', '.today .t ul li:nth-child(1)>h1::text')
        day.add_css('weather', '.today .t ul li:nth-child(1)>.wea::text')
        day.add_css('sky', '.today .t ul li:nth-child(1)> .sky .txt.lv2::text')
        day.add_css(
            'temprature', '.today .t ul li:nth-child(1)>.tem span::text')
        day.add_css('temprature_unit',
                    '.today .t ul li:nth-child(1)>.tem em::text')
        day.add_css(
            'wind_title', '.today .t ul li:nth-child(1)>.win span::attr(title)')
        day.add_css('wind_summary',
                    '.today .t ul li:nth-child(1)>.win span::text')
        # yield day.load_item()

        night = MainLoader(item=WeatherItem(), response=response)
        night.add_css('title', '.today .t ul li:nth-child(2)>h1::text')
        night.add_css('weather', '.today .t ul li:nth-child(2)>.wea::text')
        night.add_css(
            'sky', '.today .t ul li:nth-child(2)> .sky .txt.lv2::text')
        night.add_css(
            'temprature', '.today .t ul li:nth-child(2)>.tem span::text')
        night.add_css('temprature_unit',
                      '.today .t ul li:nth-child(2)>.tem em::text')
        night.add_css(
            'wind_title', '.today .t ul li:nth-child(2)>.win span::attr(title)')
        night.add_css('wind_summary',
                      '.today .t ul li:nth-child(2)>.win span::text')

        ti = TodayLoader(item=TodayItem(), response=response)
        ti.add_value('daytime_weather', day.load_item())
        ti.add_value('nighttime_weather', night.load_item())
        ti.add_css('sun_up_at', '.today .t ul li .sun span::text')
        ti.add_css('sun_down_at', '.today .t ul li .sun span::text')
        # ti.add_value('date', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        # logging.warning("aaa")
        # logging.warning(ti.load_item())
        return ti.load_item()
        # ti = TodayItem()
        # ti.daytime_weather = day.load_item()
        # ti.nighttime_weather = night.load_item()
        # ti.sun_up_at = response.css('.today .t ul li .sun span::text').get()
        # ti.sun_down_at = response.css('.today .t ul li .sun span::text').get()
        # ti.date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # yield ti
