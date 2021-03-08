# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import os

import pymysql
from bs4 import BeautifulSoup

from djangoProject.settings import BASE_DIR
from sougou_weixin.logger import logger
from api.serializers import ArticleSerializer, KeywordArticleSerializer
from sougou_weixin.sougou_weixin import get_keyword, n_digits_random, add_scrapedUrls

# 配置scrapy爬虫logger
scrapy_log = logger('scrapy.log', logging.DEBUG, logging.DEBUG)


class MyscrapyPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='39.102.58.35',  # 数据库地址
            port=3306,  # 数据库端口
            db='crawler',  # 数据库名
            user='root',  # 数据库用户名
            passwd='jsjs=123',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor();


    def process_item(self, item, spider):
        keyword = get_keyword()
        saved_flag = False
        for word in keyword:
            if word['keyword'] in item['title'] or word['keyword'] in item['text']:
                article_id = 0
                if not saved_flag:
                    dir_name = n_digits_random(4)
                    first = os.path.join(BASE_DIR, 'local')
                    second = os.path.join(first, item['target'])
                    third = os.path.join(second, item['time'])
                    target_dir = os.path.join(third, dir_name + '/')
                    if not os.path.exists(first):  # 不存在则创建路径
                        os.mkdir(first)
                    if not os.path.exists(second):
                        os.mkdir(second)
                    if not os.path.exists(third):
                        os.mkdir(third)
                    if not os.path.exists(target_dir):
                        os.mkdir(target_dir)

                    filepath = target_dir + dir_name + '.html'
                    relative_dir = 'local/' + item['target'] + '/' + item['time'] + '/' + dir_name + '/'
                    relative_filepath = relative_dir + dir_name + '.html'
                    filepath_bak = target_dir + dir_name + '_bak.html'

                    try:
                        with open(filepath, 'wb') as fp:
                            fp.write(item['response'].body)
                    except:
                        scrapy_log.info("failed save to local file")
                    else:
                        scrapy_log.info("successfully saved to local file")

                    self.cursor.execute(
                        """insert into api_article(target, url, title, time ,text, filepath)
                        value (%s, %s, %s, %s, %s, %s)""",
                        (item['target'],
                         item['url'],
                         item['title'],
                         item['time'],
                         item['text'],
                         relative_filepath))

                    # 提交sql语句
                    article_id = int(self.connect.insert_id())
                    try:
                        self.connect.commit()
                    except:
                        scrapy_log.error("failed save to database")
                    else:
                         add_scrapedUrls(item['url'], item['time'])
                         saved_flag = True
                         scrapy_log.info("successfully saved to database")

                self.cursor.execute(
                    """insert into api_keywordarticle(keyword_id, article_id)
                    value (%s, %s)""",
                    (word['keyword_id'],
                     article_id))
                try:
                    self.connect.commit()
                except:
                    scrapy_log.error("keyword-article relationship built failed!")
                else:
                    pass
        if not saved_flag:
            scrapy_log.info(item['target'] + " not contains any of the keywords, pass")

        return item

