from api.models import Keyword, ScrapedUrls, Target
from api.serializers import KeywordSerializer, ScrapedUrlsSerializer


def get_keyword():
    title = []
    text = []
    querysetTitle = Keyword.objects.filter(type=1)
    querysetText = Keyword.objects.filter(type=2)
    serializerTitle = KeywordSerializer(querysetTitle, many=True)
    serializerText = KeywordSerializer(querysetText, many=True)
    for keyword in serializerTitle.data:
        title.append(keyword['keyword'])
    for keyword in serializerText.data:
        text.append(keyword['keyword'])
    key_word = {
        'title': title,
        'text': text
    }
    return key_word


def match_keyword(content, key_word):
    for key_word_title in key_word:
        if key_word_title in content:
            return True
    return False

def not_in_scrapedUrls(url):
    queryset = ScrapedUrls.objects.filter(url=url)
    if queryset:
        return False
    return True

def add_scrapedUrls(url):
    data = {
        'url': url
    }
    serializer = ScrapedUrlsSerializer(data=data)
    if serializer.is_valid():
        # 调用save(), 从而调用序列化对象的create()方法,创建一条数据
        serializer.save()
