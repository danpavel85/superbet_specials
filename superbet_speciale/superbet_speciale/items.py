# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DaNuItem(scrapy.Item):
	s_id=scrapy.Field()
	group_name = scrapy.Field()
	odd_name=scrapy.Field()
	da=scrapy.Field()
	nu=scrapy.Field()

class InainteDupaItem(scrapy.Item):
	s_id=scrapy.Field()
	group_name = scrapy.Field()
	odd_name=scrapy.Field()
	minutul=scrapy.Field()
	inainte=scrapy.Field()
	dupa=scrapy.Field()

class F1x2Item(scrapy.Item):
	s_id=scrapy.Field()
	group_name = scrapy.Field()
	odd_name=scrapy.Field()
	_1=scrapy.Field()
	_x=scrapy.Field()
	_2=scrapy.Field()

class TotaluriItem(scrapy.Item):
	s_id=scrapy.Field()
	group_name = scrapy.Field()
	odd_name=scrapy.Field()
	sbval=scrapy.Field()
	sub=scrapy.Field()
	peste=scrapy.Field()