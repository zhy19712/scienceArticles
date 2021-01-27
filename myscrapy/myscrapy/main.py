import sys
import os

from scrapy import cmdline
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
cmdline.execute('scrapy crawl wechatSpider'.split())