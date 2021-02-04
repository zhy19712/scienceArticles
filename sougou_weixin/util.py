import datetime
import random

from api.models import Target, ScrapedUrls, Keyword
from api.serializers import TargetSerializer, ScrapedUrlsSerializer, KeywordSerializer, KeywordArticleSerializer


# 获取爬取对象
# target_type = 2 ：微信公众号 ['name1','name2']
# target_type = 1 ：网站 ['url1','url2']
def get_target(type):
    target = []
    queryset = Target.objects.filter(type=type, status=1).distinct()
    serializer = TargetSerializer(queryset, many=True)
    for row in serializer.data:
            target.append(row['target'])
    return list(set(target))


# 时间戳转时间字符串
def timestamp2string(timeStamp):
    try:
        d = datetime.datetime.fromtimestamp(timeStamp)
        # str1 = d.strftime("%Y-%m-%d %H:%M:%S.%f")
        str1 = d.strftime("%Y-%m-%d %H:%M:%S")
        # 2015-08-28 16:43:37.283000'
        return str1
    except Exception as e:
        print(e)
        return ''


# 判断文章是否已经存在
def not_in_scrapedUrls(target, time):
    queryset = ScrapedUrls.objects.filter(name=target, time=time)
    if queryset:
        return False
    return True


# 标记已入库文章
def add_scrapedUrls(target, time):
    data = {
        'name': target,
        'time': time
    }
    serializer = ScrapedUrlsSerializer(data=data)
    if serializer.is_valid():
        serializer.save()


# 产生N位随机数
def n_digits_random(n):
    seeds = "1234567890"
    random_num = []
    for i in range(n):
        random_num.append(random.choice(seeds))
    # 将列表里的值，变成四位字符串
    return "" . join(random_num)


def match_keyword(type, content):
    keyword = []
    queryset = Keyword.objects.filter(type=type, status=1)
    serializer = KeywordSerializer(queryset, many=True)
    for row in serializer.data:
        keyword.append({'keyword':row['keyword'],'keyword_id':row['id']})

    for word in keyword:
        if word['keyword'] in content:
            data = {
                "keyword_id" : word['keyword_id'],
                "article_id" : 2
            }
            serializer = KeywordArticleSerializer(data=data)
            print(data)
            if serializer.is_valid():
                serializer.save()


