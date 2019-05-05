# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanSpiderItem(scrapy.Item):
    rank = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    director = scrapy.Field()
    screenwriter = scrapy.Field()
    stars = scrapy.Field()
    types = scrapy.Field()
    runtime = scrapy.Field()
    IMDb = scrapy.Field()
    origin_url = scrapy.Field()
    pub_time = scrapy.Field()

