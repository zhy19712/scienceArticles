from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import TargetSerializer
from api.models import Target


class TargetView(APIView):
    def post(self, request):

        serializer = TargetSerializer(data=request.data)
        if serializer.is_valid():
            if not Target.objects.filter(target=request.data['target']):
                target = serializer.save()
                response = {
                    'code': 1,
                    'data': serializer.data,
                }
                return Response(response)
            else:
                response = {
                    'code': 1,
                    'data': ['目标已存在']
                }
                return Response(response)
        else:
            return Response(serializer.errors)

    def get(self, request):
        target = Target.objects.all()
        serializer = TargetSerializer(target, many=True)
        response = {
            'code': 1,
            'data': serializer.data,
        }
        return Response(response)

    def put(self, request):
        page = request.data['page']
        size = request.data['size']
        # count = request.data['count']
        target = Target.objects.all()[(page-1)*size:page*size]
        count = Target.objects.count()
        serializer = TargetSerializer(target, many=True)
        response = {
            'code': 1,
            'data': serializer.data,
            'count': count
        }
        return Response(response)


class TargetFilterView(APIView):
    def post(self, request):
        uid = request.data['id']
        target = Target.objects.get(id=uid)
        serializer = TargetSerializer(target)
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
            target = Target.objects.get(id=uid)
        except:
            response = {
                'code': 0,
                'data': [],
            }
            return Response(response)
        else:
            serializer = TargetSerializer(data=request.data, instance=target)
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
            Target.objects.get(id=uid).delete()
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

