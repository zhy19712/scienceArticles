# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from api import models


class TutorialItem(DjangoItem):
    django_model = models.Article


class CtgItem(DjangoItem):
    django_model = models.Article

