from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import CategorySerializer
from api.models import Category, Keyword


class CategoryView(APIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            if not Category.objects.filter(category=request.data['category'], center_id=request.data['center_id']):
                category = serializer.save()
                response = {
                    'code': 1,
                    'data': serializer.data,
                }
                return Response(response)
            else:
                response = {
                    'code': 0,
                    'message': '分类已存在'
                }
                return Response(response)
        else:
            return Response(serializer.errors)

    def get(self, request):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        response = {
            'code': 1,
            'data': serializer.data,
        }
        return Response(response)

    def put(self, request):
        page = request.data['page']
        size = request.data['size']
        center_id = request.data['center_id']
        category = Category.objects.filter(center_id=center_id)[(page-1)*size:page*size]
        queryset = Category.objects.filter(center_id=center_id)
        serializer = CategorySerializer(category, many=True)
        queryset_serializer = CategorySerializer(queryset, many=True)
        count = len(queryset_serializer.data)
        response = {
            'code': 1,
            'data': serializer.data,
            'count': count
        }
        return Response(response)


class CategoryFilterView(APIView):
    # 选择中心，获取该中心下的分类
    def post(self, request):
        center_id = request.data['center_id']
        category = Category.objects.filter(center_id=center_id)
        serializer = CategorySerializer(category, many=True)
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
        count = Category.objects.filter(category=request.data['category'], center_id=request.data['center_id']).exclude(id=uid).count()
        if count > 0:
            response = {
                'code': 0,
                'message': 'category 已存在',
            }
            return Response(response)
        else:
            try:
                category = Category.objects.get(id=uid)
            except:
                response = {
                    'code': 0,
                    'message': 'id 不存在',
                }
                return Response(response)
            else:
                serializer = CategorySerializer(data=request.data, instance=category)
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
            Category.objects.get(id=uid).delete()
        except:
            response = {
                'code': 0,
                'message': 'id不存在',
            }
            return Response(response)
        else:
            Keyword.objects.filter(category_id=uid).delete()
            response = {
                'code': 1,
                'message': '删除成功',
            }
            return Response(response)

