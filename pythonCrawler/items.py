# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PythoncrawlerItem(scrapy.Item):
    company_name = scrapy.Field()
    title = scrapy.Field()
    job = scrapy.Field()
    deadline = scrapy.Field()
    career = scrapy.Field()
    company_info = scrapy.Field()
    homepage = scrapy.Field()
    achievement = scrapy.Field()
    area = scrapy.Field()
    # author_name = scrapy.Field()
    # text = scrapy.Field()
    # tags = scrapy.Field()
    pass
