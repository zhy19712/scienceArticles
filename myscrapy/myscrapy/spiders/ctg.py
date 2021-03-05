import datetime
import logging
import os
import re

import scrapy
from bs4 import BeautifulSoup

from logger import logger
from myscrapy.items import ArticleItem
from scrapy import Request

from djangoProject.settings import BASE_DIR
from serializers import ArticleSerializer, KeywordArticleSerializer
from sougou_weixin.util import get_keyword, not_in_scrapedUrls, n_digits_random, get_domain, is_time, add_scrapedUrls




class CtgSpider(scrapy.Spider):
    name = 'ctg_spider'  # 项目名称
    domains = []
    start_urls = ['https://www.ctg.com.cn']  # 开始url
    for url in start_urls:
        domains.append(get_domain(url))
    allowed_domains = domains  #指定爬虫作用范围

    def parse(self, response):
        all_urls = re.findall('href="(.*?)"', response.xpath("/html").extract_first())
        for url in all_urls:
            item = ArticleItem()
            if re.findall("(\.docx)|(\.doc)|(\.pdf)|(\.jpg)|(\.jpeg)|(\.gif)|(\.ico)|(\.png)|(\.js)|(\.css)$", url.strip()):
                pass  # 去掉无效链接
            elif url.strip().startswith("http") or url.strip().startswith("/"):
                temp_url = url.strip() if url.strip().startswith('http') else 'https://' + get_domain(response.url) + url.strip()  # 三目运算符获取完整网址
                item = self.get_all(item, response)
                yield item  # 发送到管道
                yield Request(temp_url, callback=self.parse)  # 递归调用

    def get_all(self, item, response):
        url = response.url.strip()
        print(response.html)
        if not_in_scrapedUrls(url, "2021", 1):
            # 获取当前页面的网址、title、一级标题、正文内容
            main_text = []
            text = ''
            # 路径1
            title = response.xpath('/html/head/title/text()').extract()[0].strip()
            title = title[:-12]
            # 路径2
            # title = response.xpath("//h1/span[@class='title-info-title']/text()").extract()
            # if title:
            #     title = title[0]
            try:
                temp_time = re.findall('\d+', response.xpath("//p[@class='date']/text()").extract()[0])
            except:
                time = datetime.date.today()
            else:
                time = temp_time[0] + '-' + temp_time[1] + '-' + temp_time[2]

            for tag in ['p', 'br']:
                sub_text = self.get_content(response, tag)
                main_text.extend(sub_text)
            # 对正文内容去重并判断不为空
            # main_text = list(set(main_text))
            if len(main_text) != 0:
                text = '\n'.join(main_text)
            if text != '' and title != '':
                item['target'] = get_domain(url)
                item['url'] = url
                item['title'] = title
                item['time'] = time
                item['text'] = text
                item['response'] = response
                return item
            else:
                pass


    def get_content(self, response, tag):
        # 判断只有大于1个文字的内容才保留
        main_text = []
        contexts = response.xpath('//*[@id="996068e16a59465c8e903c48b612dfe7"]/div[2]/div[4]/div/' + tag + '/text()').extract()
        for text in contexts:
            if len(text.strip()) > 10:
                main_text.append(text.strip())
        return main_text


