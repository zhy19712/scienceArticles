# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from api import models


class MyscrapyItem(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # ip = scrapy.Field()
    # port = scrapy.Field()
    # typ = scrapy.Field()
    # protocal = scrapy.Field()
    # position = scrapy.Field()
    django_model = models.Proxy


class TutorialItem(DjangoItem):
    django_model = models.Article


class CtgItem(DjangoItem):
    django_model = models.Article

