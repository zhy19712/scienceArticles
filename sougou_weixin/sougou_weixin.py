import os
import time
from urllib import parse

from bs4 import BeautifulSoup


from api.serializers import ArticleSerializer, KeywordArticleSerializer
from djangoProject.settings import BASE_DIR
from djangoProject.logger import logger
from sougou_weixin.util import not_in_scrapedUrls, add_scrapedUrls, n_digits_random, get_target, get_keyword, \
    timestamp2date
import logging
import re
import random
import json
import requests
from lxml import etree
from apscheduler.schedulers.background import BackgroundScheduler

# 配置微信爬虫logger
weixin_log = logger('weixin.log', logging.DEBUG, logging.DEBUG)
article_time = ''
article_url = ''


def get_start_cookie(url, UserAgent):
    headers1 = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Host": "weixin.sogou.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": UserAgent,
    }
    response = requests.get(url, headers=headers1)
    SetCookie = response.headers['Set-Cookie']
    cookie_params = {
        "ABTEST": re.findall('ABTEST=(.*?);', SetCookie, re.S)[0],
        "SNUID": re.findall('SNUID=(.*?);', SetCookie, re.S)[0],
        "IPLOC": re.findall('IPLOC=(.*?);', SetCookie, re.S)[0],
        "SUID": re.findall('SUID=(.*?);', SetCookie, re.S)[0]
    }
    return cookie_params


def get_cookie(response1, uigs_para, UserAgent):
    SetCookie = response1.headers['Set-Cookie']
    cookie_params = {
        "ABTEST": re.findall('ABTEST=(.*?);', SetCookie, re.S)[0],
        "SNUID": re.findall('SNUID=(.*?);', SetCookie, re.S)[0],
        "IPLOC": re.findall('IPLOC=(.*?);', SetCookie, re.S)[0],
        "SUID": re.findall('SUID=(.*?);', SetCookie, re.S)[0]
    }

    url = "https://www.sogou.com/sug/css/m3.min.v.7.css"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": "SNUID={}; IPLOC={}".format(cookie_params['SNUID'], cookie_params['IPLOC']),
        "Host": "www.sogou.com",
        "Referer": "https://weixin.sogou.com/",
        "User-Agent": UserAgent
    }
    response2 = requests.get(url, headers=headers)
    SetCookie = response2.headers['Set-Cookie']
    cookie_params['SUID'] = re.findall('SUID=(.*?);', SetCookie, re.S)[0]

    url = "https://weixin.sogou.com/websearch/wexinurlenc_sogou_profile.jsp"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": "ABTEST={}; SNUID={}; IPLOC={}; SUID={}".format(cookie_params['ABTEST'], cookie_params['SNUID'],
                                                                  cookie_params['IPLOC'],
                                                                  cookie_params['SUID']),
        "Host": "weixin.sogou.com",
        "Referer": response1.url,
        "User-Agent": UserAgent
    }
    response3 = requests.get(url, headers=headers)
    SetCookie = response3.headers['Set-Cookie']
    cookie_params['JSESSIONID'] = re.findall('JSESSIONID=(.*?);', SetCookie, re.S)[0]

    url = "https://pb.sogou.com/pv.gif"
    headers = {
        "Accept": "image/webp,*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": "SNUID={}; IPLOC={}; SUID={}".format(cookie_params['SNUID'], cookie_params['IPLOC'],
                                                       cookie_params['SUID']),
        "Host": "pb.sogou.com",
        "Referer": "https://weixin.sogou.com/",
        "User-Agent": UserAgent
    }
    response4 = requests.get(url, headers=headers, params=uigs_para)
    SetCookie = response4.headers['Set-Cookie']
    cookie_params['SUV'] = re.findall('SUV=(.*?);', SetCookie, re.S)[0]
    return cookie_params


def get_k_h(url):
    b = int(random.random() * 100) + 1
    a = url.find("url=")
    url = url + "&k=" + str(b) + "&h=" + url[a + 4 + 21 + b: a + 4 + 21 + b + 1]
    return url


def get_uigs_para(response):
    try:
        uigs_para = re.findall('var uigs_para = (.*?);', response.text, re.S)[0]
        if 'passportUserId ? "1" : "0"' in uigs_para:
            uigs_para = uigs_para.replace('passportUserId ? "1" : "0"', '0')
        uigs_para = json.loads(uigs_para)
        exp_id = re.findall('uigs_para.exp_id = "(.*?)";', response.text, re.S)[0]
        uigs_para['right'] = 'right0_0'
        uigs_para['exp_id'] = exp_id[:-1]
    except:
        weixin_log.error("Failed get_uigs_para")
    else:
        return uigs_para


def get_response(list_url, UserAgent):
    # headers1 = {
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    #     "Accept-Encoding": "gzip, deflate, br",
    #     "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    #     "Connection": "keep-alive",
    #     # "Cookie":"ABTEST=0|1611710577|v1; IPLOC=CN1100; SUID=C2257F7C5B0CA00A000000006010C071; SUID=02DAFB72492CA20A000000006010C071; weixinIndexVisited=1; SUV=0004E05A72FBDA026010C07148DEF872; PHPSESSID=i1aandlu9kvs65b4jtq941m806; SNUID=929BCAF68B8E308BB700125E8B6E0D10; JSESSIONID=aaaLj2eoKAtuD6vOdNuCx",
    #     "Cookie":"SUV=002713CF7C40111860137A45C1627094; ABTEST=8|1611889221|v1; SNUID=3931615C21249A211450D8D92169AC27; IPLOC=CN1100; SUID=1811407C5B0CA00A0000000060137A45; JSESSIONID=aaaotLIxfB5_U7tJgMuCx; SUID=1811407C2D34990A0000000060137A45; weixinIndexVisited=1",
    #     "Host": "weixin.sogou.com",
    #     "Sec-Fetch-Dest": "document",
    #     "Sec-Fetch-Mode": "navigate",
    #     "Sec-Fetch-Site": "same-origin",
    #     "Sec-Fetch-User": "?1",
    #     "Upgrade-Insecure-Requests": "1",
    #     "User-Agent": UserAgent,
    # }
    headers1 = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Host": "weixin.sogou.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": UserAgent,
    }
    response1 = requests.get(list_url, headers=headers1)
    html = etree.HTML(response1.text)
    weixin_log.info("list url : " + response1.url)
    urls = ['https://weixin.sogou.com' + i for i in html.xpath('//*[@id="sogou_vr_11002301_box_0"]/dl[3]/dd/a/@href')]
    timestamp = int(
        re.findall('\d+', html.xpath('//*[@id="sogou_vr_11002301_box_0"]/dl[3]/dd/span/script/text()')[0])[0])
    # timestamp = html.xpath('//*[@id="sogou_vr_11002301_box_0"]/dl[3]/dd/span/script/text()')
    global article_time
    # article_time = timestamp2string(timestamp)
    article_time = timestamp2date(timestamp)

    uigs_para = get_uigs_para(response1)
    # print(uigs_para)
    params = get_cookie(response1, uigs_para, UserAgent)
    # print(params)
    approve_url = 'https://weixin.sogou.com/approve?uuid={}'.format(uigs_para['uuid'])
    headers2 = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": "ABTEST={}; IPLOC={}; SUID={}; SUV={}; SNUID={}; JSESSIONID={};".format(params['ABTEST'],
                                                                                          params['IPLOC'],
                                                                                          params['SUID'], params['SUV'],
                                                                                          params['SNUID'],
                                                                                          params['JSESSIONID']),
        "Host": "weixin.sogou.com",
        "Referer": response1.url,
        "User-Agent": UserAgent,
        "X-Requested-With": "XMLHttpRequest"
    }
    for url in urls:
        response2 = requests.get(approve_url, headers=headers2)
        url = get_k_h(url)
        headers3 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Connection": "keep-alive",
            "Cookie": "ABTEST={}; SNUID={}; IPLOC={}; SUID={}; JSESSIONID={}; SUV={}".format(params['ABTEST'],
                                                                                             params['SNUID'],
                                                                                             params['IPLOC'],
                                                                                             params['SUID'],
                                                                                             params['JSESSIONID'],
                                                                                             params['SUV']),
            "Host": "weixin.sogou.com",
            "Referer": list_url,
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": UserAgent
        }
        response3 = requests.get(url, headers=headers3)

        fragments = re.findall("url \+= '(.*?)'", response3.text, re.S)
        itemurl = ''
        for i in fragments:
            itemurl += i

        global article_url
        article_url = itemurl
        print(article_url)

        # 文章url拿正文
        headers4 = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "max-age=0",
            "user-agent": UserAgent
        }
        response4 = requests.get(itemurl, headers=headers4)
        # print(response4.status_code)
        return response4


def save_html(response, target):
    html = etree.HTML(response.text)
    title = html.xpath('//meta[@property="og:title"]/@content')[0]
    contexts = html.xpath('//*[@id="page-content"]')
    text = contexts[0].xpath('string(.)').strip()
    keyword = get_keyword()
    saved_flag = False
    for word in keyword:
        if word['keyword'] in title or word['keyword'] in text:
            if not saved_flag:
                dir_name = n_digits_random(4)
                first = os.path.join(BASE_DIR, 'local')
                second = os.path.join(first, target)
                third = os.path.join(second, article_time[:10])
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
                relative_dir = 'local/' + target + '/' + article_time[:10] + '/' + dir_name + '/'
                relative_filepath = relative_dir + dir_name + '.html'
                filepath_bak = target_dir + dir_name + '_bak.html'

                article = {
                    "target": target,
                    "url": article_url,
                    "title": title,
                    "time": article_time,
                    "text": text,
                    "filepath": relative_filepath
                }
                serializer = ArticleSerializer(data=article)
                if serializer.is_valid():
                    serializer.save()
                    add_scrapedUrls(target, article_time)
                    saved_flag = True
                    weixin_log.info("successfully saved to database")
                else:
                    weixin_log.error("failed save to database")



                try:
                    f = open(filepath, "wb")
                    f.write(response.content)
                    f.close()

                    obj = BeautifulSoup(response.content, 'lxml')  # 后面是指定使用lxml解析，lxml解析速度比较快，容错高。
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
                        r = requests.get(url)
                        t = os.path.join(target_dir, str(i) + suffix)
                        t_relative = os.path.join(relative_dir, str(i) + suffix)
                        fw = open(t, 'wb')  # 指定绝对路径
                        fw.write(r.content)  # 保存图片到本地指定目录
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
                    weixin_log.info("failed save to local file")
                else:
                    weixin_log.info("successfully saved to local file")

            keywordarticle = {
                "keyword_id": word['keyword_id'],
                "article_id": serializer.data['id']
            }
            keywordarticle_serializer = KeywordArticleSerializer(data=keywordarticle)
            if keywordarticle_serializer.is_valid():
                keywordarticle_serializer.save()
            else:
                weixin_log.error("keyword-article relationship built failed!")

    if not saved_flag:
        weixin_log.info(target + " not contains any of the keywords, pass")


def start_process():
    target = get_target(2)
    weixin_log.info(target)
    # target = ['三峡e家']
    UserAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"

    for t in target:
        time.sleep(random.randint(10, 20))
        weixin_log.info(t + " : task start")
        url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query={}&_sug_=n&_sug_type_=&page=1'.format(
            parse.quote(t))
        try:
            response = get_response(url, UserAgent)
        except:
            weixin_log.error(t + " : Failed get article")
        else:
            if not_in_scrapedUrls(t, article_time, 2):
                save_html(response, t)
            else:
                weixin_log.info("article already exists, pass")

#
# if __name__ == "__main__":
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(start_process, 'interval', minutes=1)
#     try:
#         # scheduler.remove_all_jobs()
#         scheduler.start()
#     except (KeyboardInterrupt):
#         pass
#     start_process()

def run_weixin_crawler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(start_process, 'interval', minutes=30)
    try:
        # scheduler.remove_all_jobs()
        scheduler.start()
    except (KeyboardInterrupt):
        pass
    start_process()

