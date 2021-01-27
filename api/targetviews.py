from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import TargetSerializer
from api.models import Target


class TargetView(APIView):
    def post(self, request):
        print(request.data)

        serializer = TargetSerializer(data=request.data)
        if serializer.is_valid():
            target = serializer.save()
            response = {
                'code': 1,
                'data': serializer.data,
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

