import datetime
import random
from urllib.parse import urlsplit

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


# 时间戳转时间
def timestamp2date(timeStamp):
    dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
    otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
    return  otherStyleTime


# 判断文章是否已经存在
def not_in_scrapedUrls(target, time):
    queryset = ScrapedUrls.objects.filter(target=target, time=time)
    if queryset:
        return False
    return True


# 标记已入库文章
def add_scrapedUrls(target, time):
    data = {
        'target': target,
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


def get_keyword():
    keyword = []
    queryset = Keyword.objects.filter(status=1)
    serializer = KeywordSerializer(queryset, many=True)
    for row in serializer.data:
        keyword.append({'keyword':row['keyword'],'keyword_id':row['id']})
    return keyword


def get_host(request):
    http = urlsplit(request.build_absolute_uri(None)).scheme
    # 获得当前的HTTP或HTTPS
    host = request.META['HTTP_HOST']
    # 获取当前域名
    base_url = http + '://' + host + '/'
    return base_url

