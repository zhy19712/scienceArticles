from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import CenterSerializer
from api.models import Center


class CenterView(APIView):
    def get(self, request):
        center = Center.objects.all()
        serializer = CenterSerializer(center, many=True)
        response = {
            'code': 1,
            'data': serializer.data,
        }
        return Response(response)
