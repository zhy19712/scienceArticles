from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import KeywordSerializer, CategorySerializer
from api.models import Keyword, Category


class KeywordView(APIView):
    # 新增关键字
    def post(self, request):
        serializer = KeywordSerializer(data=request.data)

        if serializer.is_valid():
            if not Keyword.objects.filter(keyword=request.data['keyword'], category_id=request.data['category_id']):
                keyword = serializer.save()
                response = {
                    'code': 1,
                    'data': serializer.data,
                }
                return Response(response)
            else:
                response = {
                    'code': 0,
                    'message': '关键字已存在'
                }
                return Response(response)
        else:
            return Response(serializer.errors)

    # 获取所有关键字
    def get(self, request):
        article = Keyword.objects.all()
        serializer = KeywordSerializer(article, many=True)
        response = {
            'code': 1,
            'data': serializer.data,
        }
        return Response(response)

    # 获取分类下的关键字并分页
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
    # 获取对应id的关键字
    def post(self, request):
        if 'id' in request.data.keys():
            id = request.data['id']
            keyword = Keyword.objects.get(id=id)
            serializer = KeywordSerializer(keyword)
        elif 'category_id' in request.data.keys():
            category_id = request.data['category_id']
            keyword = Keyword.objects.filter(category_id=category_id)
            serializer = KeywordSerializer(keyword, many=True)
        else:
            response = {
                'code': 0,
                'message': 'id or category_id is required',
            }
            return Response(response)
        if serializer:
            response = {
                'code': 1,
                'data': serializer.data,
            }
            return Response(response)
        else:
            return Response(serializer.errors)

    # 编辑
    def put(self, request):
        uid = request.data['id']
        count = Keyword.objects.filter(keyword=request.data['keyword'], category_id=request.data['category_id']).exclude(id=uid).count()
        if count > 0 :
            response = {
                'code': 0,
                'message': 'keyword 已存在',
            }
            return Response(response)
        else:
            try:
                keyword = Keyword.objects.get(id=uid)
            except:
                response = {
                    'code': 0,
                    'message': 'id 不存在',
                }
                return Response(response)
            else:
                serializer = KeywordSerializer(data=request.data, instance=keyword)
                if serializer.is_valid():
                    serializer.save()
                    response = {
                        'code': 1,
                        'data': serializer.data,
                    }
                    return Response(response)
                else:
                    return Response(serializer.errors)


    # 删除
    def delete(self, request):
        uid = request.data['id']
        try:
            Keyword.objects.get(id=uid).delete()
        except:
            response = {
                'code': 0,
                'message': 'id不存在',
            }
            return Response(response)
        else:
            response = {
                'code': 1,
                'message': '删除成功',
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
            keyword = Keyword.objects.filter(category_id=cate['id'], status=1)
            keyword_serializer = KeywordSerializer(keyword, many=True)
            for key in keyword_serializer.data:
                children.append({'label':key['keyword'],'keyword_id':key['id']})
            data.append({'label':cate['category'], 'children':children})

        response = {
            'code': 1,
            'data': data,
        }
        return Response(response)