import scrapy
import re, os

from api.models import KeywordTitle, KeywordText, ScrapedUrls
from myscrapy.items import TutorialItem
from scrapy import Request
from api.serializers import KeywordTextSerializer, KeywordTitleSerializer, ScrapedUrlsSerializer


# 在文件主目录下执行抓取：#scrapy crawl sohuSpider

class SohuSpider(scrapy.Spider):
    name = 'sohuSpider'  # 项目名称
    allowed_domains = ['www.sohu.com']  #指定爬虫作用范围
    start_urls = ['http://www.sohu.com/']  # 开始url

    def parse(self, response):
        key_word = self.get_keyword()
        all_urls = re.findall('href="(.*?)"', response.xpath("/html").extract_first())
        for url in list(set(all_urls)):
            item = TutorialItem()
            if re.findall("(\.jpg)|(\.jpeg)|(\.gif)|(\.ico)|(\.png)|(\.js)|(\.css)$", url.strip()):
                pass  # 去掉无效链接
            elif url.strip().startswith("http") or url.strip().startswith("//"):
                temp_url = url.strip() if url.strip().startswith('http') else 'http:' + url.strip()  # 三目运算符获取完整网址
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
        # 路径2
        # title = response.xpath("//h1/span[@class='title-info-title']/text()").extract()
        # if title:
        #     title = title[0]
        print(title)
        url = response.url.strip()
        if self.not_in_scrapedUrls(url):
            if self.match_keyword(title, key_word['title']):
                self.add_scrapedUrls(url)
                item['url'] = url
                item['title'] = title
                # contain_h1 = response.xpath('//h1/text()').extract()  # 获取当前网页所有一级标题
                # contain = contain_h1[0] if len(contain_h1) != 0 else ""  # 获取第一个一级标题
                item['time'] = response.xpath("//span[@class='time']/text()").extract()
                print(item['time'])
                # 遍历网页中所有p标签和br标签的内容
                for tag in ['p', 'br']:
                    sub_text = self.get_content(response, tag)
                    main_text.extend(sub_text)
                # 对正文内容去重并判断不为空
                main_text = list(set(main_text))
                if len(main_text) != 0:
                    item['text'] = '\n'.join(main_text)
        return item

    def get_content(self, response, tag):
        # 判断只有大于1个文字的内容才保留
        main_text = []
        contexts = response.xpath('//' + tag + '/text()').extract()
        for text in contexts:
            if len(text.strip()) > 1:
                main_text.append(text.strip())
        return main_text

    def get_keyword(self):
        title = []
        text = []
        querysetTitle = KeywordTitle.objects.all()
        serializerTitle = KeywordTitleSerializer(querysetTitle, many=True)
        for keyword in serializerTitle.data:
            title.append(keyword['keyword'])
        querysetText = KeywordText.objects.all()
        serializerText = KeywordTextSerializer(querysetText, many=True)
        for keyword in serializerText.data:
            text.append(keyword['keyword'])
        key_word = {
            'title': title,
            'text': text
        }
        return key_word

    def match_keyword(self, content, key_word):
        for key_word_title in key_word:
            if key_word_title in content:
                return True
        return False

    def not_in_scrapedUrls(self, url):
        queryset = ScrapedUrls.objects.filter(url=url)
        if queryset:
            return False
        return True

    def add_scrapedUrls(self, url):
        data = {
            'url': url
        }
        serializer = ScrapedUrlsSerializer(data=data)
        if serializer.is_valid():
            # 调用save(), 从而调用序列化对象的create()方法,创建一条数据
            serializer.save()


