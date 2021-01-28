import datetime
from api.models import Target, ScrapedUrls
from api.serializers import TargetSerializer, ScrapedUrlsSerializer


# 获取爬取对象
# target_type = 2 ：微信公众号 ['name1','name2']
# target_type = 1 ：网站 ['url1','url2']
def get_target(target_type):
    target = []
    queryset = Target.objects.filter(type=target_type).distinct()
    serializer = TargetSerializer(queryset, many=True)
    for row in serializer.data:
        if target_type == 1:
            target.append(row['url'])
        else:
            target.append(row['name'])
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
