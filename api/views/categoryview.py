from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import CategorySerializer
from api.models import Category


class CategoryView(APIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            if not Category.objects.filter(category=request.data['category']):
                category = serializer.save()
                response = {
                    'code': 1,
                    'data': serializer.data,
                }
                return Response(response)
            else:
                response = {
                    'code': 1,
                    'data': ['分类已存在']
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
        # count = request.data['count']
        category = Category.objects.all()[(page-1)*size:page*size]
        count = Category.objects.count()
        serializer = CategorySerializer(category, many=True)
        response = {
            'code': 1,
            'data': serializer.data,
            'count': count
        }
        return Response(response)


class CategoryFilterView(APIView):
    def post(self, request):
        uid = request.data['id']
        category = Category.objects.get(id=uid)
        serializer = CategorySerializer(category)
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
            category = Category.objects.get(id=uid)
        except:
            response = {
                'code': 0,
                'data': [],
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
                'data': [],
            }
            return Response(response)
        else:
            response = {
                'code': 1,
                'data': [],
            }
            return Response(response)

