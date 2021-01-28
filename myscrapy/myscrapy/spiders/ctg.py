import datetime
import re

import scrapy

from myscrapy import util
from myscrapy.items import CtgItem
from scrapy import Request



class CtgSpider(scrapy.Spider):
    name = 'ctg_spider'  # 项目名称
    allowed_domains = ['www.ctg.com.cn']  #指定爬虫作用范围
    start_urls = ['https://www.ctg.com.cn/']  # 开始url

    def parse(self, response):
        key_word = util.get_keyword()
        all_urls = re.findall('href="(.*?)"', response.xpath("/html").extract_first())
        for url in all_urls:
            item = CtgItem()
            if re.findall("(\.docx)|(\.doc)|(\.pdf)|(\.jpg)|(\.jpeg)|(\.gif)|(\.ico)|(\.png)|(\.js)|(\.css)$", url.strip()):
                pass  # 去掉无效链接
            elif url.strip().startswith("http") or url.strip().startswith("/"):
                temp_url = url.strip() if url.strip().startswith('http') else 'https://www.ctg.com.cn' + url.strip()  # 三目运算符获取完整网址
                item = self.get_all(item, response, key_word)
                # 判断item中存在正文且不为空，页面一级标题不为空
                if 'text' in item and item['text'] != '' and item['title'] != '':

                    yield item  # 发送到管道
                yield Request(temp_url, callback=self.parse)  # 递归调用

    def get_all(self, item, response, key_word):
        # 获取当前页面的网址、title、一级标题、正文内容
        main_text = []
        # 路径1
        title = response.xpath('/html/head/title/text()').extract()[0].strip()
        title = title[:-12]
        # 路径2
        # title = response.xpath("//h1/span[@class='title-info-title']/text()").extract()
        # if title:
        #     title = title[0]
        url = response.url.strip()
        if util.not_in_scrapedUrls(url):
            if util.match_keyword(title, key_word['title']):
            # if 1 == 1:
                util.add_scrapedUrls(url)
                item['source'] = 'www.ctg.com.cn'
                item['url'] = url
                item['title'] = title
                time = re.findall('\d+', response.xpath("//p[@class='date']/text()").extract()[0])
                item['time'] = time[0] + '-' + time[1] + '-' + time[2]

                for tag in ['p', 'br']:
                    sub_text = self.get_content(response, tag)
                    main_text.extend(sub_text)
                # # 对正文内容去重并判断不为空
                # main_text = list(set(main_text))
                if len(main_text) != 0:
                    item['text'] = '\n'.join(main_text)
        return item

    def get_content(self, response, tag):
        # 判断只有大于1个文字的内容才保留
        main_text = []
        contexts = response.xpath('//*[@id="996068e16a59465c8e903c48b612dfe7"]/div[2]/div[4]/div/' + tag + '/text()').extract()
        for text in contexts:
            if len(text.strip()) > 10:
                main_text.append(text.strip())
        return main_text
