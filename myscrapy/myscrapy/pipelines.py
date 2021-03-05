# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import os

from bs4 import BeautifulSoup
from itemadapter import ItemAdapter


#
# class MyscrapyPipeline:
#     def process_item(self, item, spider):
#         return item
from djangoProject.settings import BASE_DIR
from logger import logger
from api.serializers import ArticleSerializer, KeywordArticleSerializer
from sougou_weixin.util import get_keyword, n_digits_random, add_scrapedUrls

# 配置scrapy爬虫logger
scrapy_log = logger('scrapy.log', logging.DEBUG, logging.DEBUG)


class MyscrapyPipeline(object):
    def process_item(self, item, spider):
        keyword = get_keyword()
        saved_flag = False
        for word in keyword:
            if word['keyword'] in item['title'] or word['keyword'] in item['text']:
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

                    article = {
                        "target": item['target'],
                        "url": item['url'],
                        "title": item['title'],
                        "time": item['time'],
                        "text": item['text'],
                        "filepath": relative_filepath
                    }
                    serializer = ArticleSerializer(data=article)

                    if serializer.is_valid():
                        serializer.save()
                        add_scrapedUrls(item['url'], item['time'])
                        saved_flag = True
                        scrapy_log.info("successfully saved to database")
                    else:
                        scrapy_log.error("failed save to database")

                    try:
                        f = open(filepath, "wb")
                        f.write(item['response'].content)
                        f.close()

                        obj = BeautifulSoup(item['response'].content, 'lxml')  # 后面是指定使用lxml解析，lxml解析速度比较快，容错高。
                        imgs = obj.find_all('img')
                        urls = []
                        for img in imgs:
                            if 'data-src' in str(img):
                                urls.append(img['data-src'])
                        # 遍历所有图片链接，将图片保存到本地指定文件夹，图片名字用0，1，2...
                        i = 0
                        suffix = ''
                        for url in urls:
                            if url.endswith('png'):
                                suffix = '.png'
                            elif url.endswith('jpeg'):
                                suffix = '.jpg'
                            elif url.endswith('gif'):
                                suffix = '.gif'
                            t = os.path.join(target_dir, str(i) + suffix)
                            t_relative = os.path.join(relative_dir, str(i) + suffix)
                            fw = open(t, 'wb')  # 指定绝对路径
                            fw.write(item['response'].content)  # 保存图片到本地指定目录
                            i += 1

                            with open(filepath, encoding='utf-8') as f, open(filepath_bak, 'w',
                                                                             encoding='utf-8') as fw:  # 打开两个文件，原始文件用来读，另一个文件将修改的内容写入
                                old_url = 'data-src="' + url + '"'
                                new_url = 'src="/' + t_relative + '"'
                                for line in f:  # 遍历每行，用replace 方法替换
                                    new_line = line.replace(old_url, new_url)  # 逐行替换
                                    fw.write(new_line)  # 写入新文件
                            os.remove(filepath)  # 删除原始文件
                            os.rename(filepath_bak, filepath)  # 修改新文件名， old -> new

                            fw.close()
                    except:
                        scrapy_log.info("failed save to local file")
                    else:
                        scrapy_log.info("successfully saved to local file")

                keywordarticle = {
                    "keyword_id": word['keyword_id'],
                    "article_id": serializer.data['id']
                }
                keywordarticle_serializer = KeywordArticleSerializer(data=keywordarticle)
                if keywordarticle_serializer.is_valid():
                    keywordarticle_serializer.save()
                else:
                    scrapy_log.error("keyword-article relationship built failed!")

        if not saved_flag:
            scrapy_log.info(item['target'] + " not contains any of the keywords, pass")

        return item

