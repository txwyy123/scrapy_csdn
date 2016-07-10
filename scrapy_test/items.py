# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class CsdnSpiderItem(Item):
    # define the fields for your item here like:
    # nam∑e = scrapy.Field()
    id = Field()
    url = Field()
    title = Field()
    read_count = Field()
    comment_count = Field()
