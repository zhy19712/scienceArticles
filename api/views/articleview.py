from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import ArticleSerializer, KeywordArticleSerializer
from api.models import Article, KeywordArticle


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

    def put(self, request):
        page = request.data['page']
        size = request.data['size']
        keyword_id = request.data['keyword_id']
        article_id = []
        queryset = KeywordArticle.objects.filter(keyword_id=keyword_id)
        serializer = KeywordArticleSerializer(queryset, many=True)
        for row in serializer.data:
            article_id.append(row['article_id'])

        print(article_id)

        # count = request.data['count']
        article = Article.objects.filter(id__in=article_id)[(page-1)*size:page*size]

        serializer = ArticleSerializer(article, many=True)
        response = {
            'code': 1,
            'data': serializer.data,
            'count': 0
        }
        return Response(response)


class ArticleFilterView(APIView):
    def post(self, request):
        uid = request.data['id']
        article = Article.objects.get(id=uid)
        serializer = ArticleSerializer(article)
        if serializer:
            response = {
                'code': 1,
                'data': serializer.data,
            }
            return Response(response)
        else:
            return Response(serializer.errors)

    def put(self, request):
        uid = request.data['id']
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
        uid = request.data['id']
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

