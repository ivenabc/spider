# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity,Join





class City(Item):
    province = Field()
    cityid = Field()
    cityname = Field()


class WeatherItem(Item):
    index = Field()
    title = Field()
    weather = Field()
    sky = Field()
    temprature = Field()
    max_temprature = Field()
    min_temprature = Field()
    temprature_unit = Field()
    wind_summary = Field()
    wind = Field(output_processor=Identity())


class TodayItem(Item):
    daytime_weather = Field(serializer=WeatherItem)
    nighttime_weather = Field(serializer=WeatherItem)
    sun_up_at = Field()
    sun_down_at = Field()
    date = Field()


class MainLoader(ItemLoader):
    # default_item_class = WeatherItem
    default_output_processor = TakeFirst()


class TodayLoader(ItemLoader):
    default_item_class = WeatherItem
    default_output_processor = TakeFirst()