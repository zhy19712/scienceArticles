from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import KeywordSerializer
from api.models import Keyword


class KeywordView(APIView):
    def post(self, request):
        print(request.data)

        serializer = KeywordSerializer(data=request.data)
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
        article = Keyword.objects.all()
        serializer = KeywordSerializer(article, many=True)
        response = {
            'code': 1,
            'data': serializer.data,
        }
        return Response(response)


class KeywordFilterView(APIView):
    def post(self, request):
        uid = request.data['id']
        article = Keyword.objects.get(id=uid)
        serializer = KeywordSerializer(article)
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
            article = Keyword.objects.get(id=uid)
        except:
            response = {
                'code': 0,
                'data': [],
            }
            return Response(response)
        else:
            serializer = KeywordSerializer(data=request.data, instance=article)
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

