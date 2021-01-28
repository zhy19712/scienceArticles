import time
from urllib import parse
from logger import logger
from serializers import ArticleSerializer
from util import get_target, timestamp2string, not_in_scrapedUrls, add_scrapedUrls
import logging
import re
import random
import json
import requests
from lxml import etree

# 配置微信爬虫logger
weixin_log = logger('weixin.log', logging.DEBUG, logging.DEBUG)
article_time = ''
article_url = ''



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
        "Accept": "text/css,*/*;q=0.1",
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
        weixin_log.info("uigs_para list index out of range")
    else:
        return uigs_para


def get_article(list_url, UserAgent):
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
    print(response1.url)
    urls = ['https://weixin.sogou.com' + i for i in html.xpath('//*[@id="sogou_vr_11002301_box_0"]/dl[3]/dd/a/@href')]
    timestamp = int(re.findall('\d+', html.xpath('//*[@id="sogou_vr_11002301_box_0"]/dl[3]/dd/span/script/text()')[0])[0])
    # timestamp = html.xpath('//*[@id="sogou_vr_11002301_box_0"]/dl[3]/dd/span/script/text()')
    global article_time
    article_time = timestamp2string(timestamp)

    uigs_para = get_uigs_para(response1)
    params = get_cookie(response1, uigs_para, UserAgent)
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

        # 文章url拿正文
        headers4 = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "max-age=0",
            "user-agent": UserAgent
        }
        response4 = requests.get(itemurl, headers=headers4)
        html = etree.HTML(response4.text)
        weixin_log.info(response4.status_code)
        return html



if __name__ == "__main__":
    target = get_target(2)
    print(target)
    # target = ['科技富能量']
    UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"
    for t in target:
        time.sleep(5)
        weixin_log.info(t)
        weixin_log.info("task start!")
        url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query={}&_sug_=n&_sug_type_=&page=1'.format(parse.quote(t))
        try:
            html = get_article(url, UserAgent)
        except:
            weixin_log.info(t+" : Error processing request!")
        else:
            if not_in_scrapedUrls(t, article_time):
                add_scrapedUrls(t, article_time)
                title = html.xpath('//meta[@property="og:title"]/@content')[0]
                contexts = html.xpath('//*[@id="js_content"]')
                text = contexts[0].xpath('string(.)').strip()

                article = {
                    "source": t,
                    "url": article_url,
                    "title": title,
                    "time": article_time,
                    "text": text
                }
                serializer = ArticleSerializer(data=article)
                if serializer.is_valid():
                    serializer.save()
                    add_scrapedUrls(t, article_time)
                    weixin_log.info("task completed!")
                else:
                    weixin_log.info("failed save to database!")
            else:
                weixin_log.info("article already exists, pass")







