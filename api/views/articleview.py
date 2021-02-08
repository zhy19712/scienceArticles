from urllib.parse import urlsplit

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import ArticleSerializer, KeywordArticleSerializer
from api.models import Article, KeywordArticle
from sougou_weixin.util import get_host


class ArticleView(APIView):
    def post(self, request):
        print(request.data)

        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            article = serializer.save()
            response = {
                'code': 1,
                'data': serializer.data,
            }
            return Response(response)
        else:
            return Response(serializer.errors)

    def get(self, request):
        article = Article.objects.all()
        serializer = ArticleSerializer(article, many=True)
        response = {
            'code': 1,
            'data': serializer.data,
        }
        return Response(response)

    # 通过keyword_id查询关键字所对应的文章
    def put(self, request):
        if 'page' in request.data.keys():
            page = request.data['page']
        if 'size' in request.data.keys():
            size = request.data['size']
        if 'keyword_id' in request.data.keys():
            keyword_id = request.data['keyword_id']
        article_id = []
        queryset = KeywordArticle.objects.filter(keyword_id=keyword_id)
        serializer = KeywordArticleSerializer(queryset, many=True)
        for row in serializer.data:
            article_id.append(row['article_id'])

        article = Article.objects.filter(id__in=article_id)[(page-1)*size:page*size]
        article_all = Article.objects.filter(id__in=article_id)

        serializer = ArticleSerializer(article, many=True)
        serializer_all = ArticleSerializer(article_all, many=True)
        count = len(serializer_all.data)

        response = {
            'code': 1,
            'data': serializer.data,
            'count': count
        }
        return Response(response)


class ArticleFilterView(APIView):
    def post(self, request):
        if 'article_id' in request.data.keys():
            article_id = request.data['article_id']
        if 'type' in request.data.keys():
            type = request.data['type']
        article = Article.objects.get(id=article_id)
        serializer = ArticleSerializer(article)
        if serializer:
            if type == 'text':
                response = {
                    'code': 1,
                    'data': serializer.data
                }
                return Response(response)
            elif type == 'html':
                base_url = get_host(request)
                response = {
                    'code': 1,
                    'data': base_url + serializer.data['filepath']
                }
                return Response(response)
        else:
            return Response(serializer.errors)



    def put(self, request):
        if 'uid' in request.data.keys():
            uid = request.data['uid']
        try:
            article = Article.objects.get(id=uid)
        except:
            response = {
                'code': 0,
                'data': [],
            }
            return Response(response)
        else:
            serializer = ArticleSerializer(data=request.data, instance=article)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'code': 1,
                    'data': serializer.data,
                }
                return Response(response)
            else:
                return Response(serializer.errors)

    def delete(self, request):
        if 'uid' in request.data.keys():
            uid = request.data['uid']
        try:
            Article.objects.get(id=uid).delete()
        except:
            response = {
                'code': 0,
                'data': [],
            }
            return Response(response)
        else:
            response = {
                'code': 1,
                'data': [],
            }
            return Response(response)


class GlobalSearchView(APIView):
    def post(self,request):
        if 'start_date' in request.data.keys():
            start_date = request.data['start_date']
        if 'end_date' in request.data.keys():
            end_date = request.data['end_date']
        if 'keyword' in request.data.keys():
            keyword = request.data['keyword']


        response = {
            'code': 1,
            'data': [start_date,end_date,keyword],
        }
        return Response(response)


