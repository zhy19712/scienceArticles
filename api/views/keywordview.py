from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import KeywordSerializer, CategorySerializer
from api.models import Keyword, Category


class KeywordView(APIView):
    def post(self, request):
        serializer = KeywordSerializer(data=request.data)

        if serializer.is_valid():
            if not Keyword.objects.filter(keyword=request.data['keyword']):
                keyword = serializer.save()
                response = {
                    'code': 1,
                    'data': serializer.data,
                }
                return Response(response)
            else:
                response = {
                    'code': 1,
                    'data': ['关键字已存在']
                }
                return Response(response)
        else:
            return Response(serializer.errors)

    def get(self, request):
        article = Keyword.objects.all()
        serializer = KeywordSerializer(article, many=True)
        response = {
            'code': 1,
            'data': serializer.data,
        }
        return Response(response)

    def put(self, request):
        page = request.data['page']
        size = request.data['size']
        category_id = request.data['category_id']
        keyword = Keyword.objects.filter(category_id=category_id)[(page-1)*size:page*size]
        queryset = Keyword.objects.filter(category_id=category_id)
        serializer = KeywordSerializer(keyword, many=True)
        queryset_serializer = KeywordSerializer(queryset, many=True)
        count = len(queryset_serializer.data)
        response = {
            'code': 1,
            'data': serializer.data,
            'count': count
        }
        return Response(response)


class KeywordFilterView(APIView):
    # 选择分类，获取分类下的关键字
    def post(self, request):
        category_id = request.data['category_id']
        keyword = Keyword.objects.filter(category_id=category_id)
        serializer = KeywordSerializer(keyword, many=True)
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
            keyword = Keyword.objects.get(id=uid)
        except:
            response = {
                'code': 0,
                'data': [],
            }
            return Response(response)
        else:
            serializer = KeywordSerializer(data=request.data, instance=keyword, many=True)
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
            Keyword.objects.get(id=uid).delete()
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


class KeywordTreeView(APIView):
    def post(self, request):
        center_id = request.data['center_id']
        category = Category.objects.filter(center_id=center_id)
        category_serializer = CategorySerializer(category, many=True)
        data = []
        for cate in category_serializer.data:
            children = []
            keyword = Keyword.objects.filter(category_id=cate['id'])
            keyword_serializer = KeywordSerializer(keyword, many=True)
            for key in keyword_serializer.data:
                children.append({'label':key['keyword'],'keyword_id':key['id']})
            data.append({'label':cate['category'], 'children':children})

        response = {
            'code': 1,
            'data': data,
        }
        return Response(response)