from rest_framework.response import Response
from rest_framework.views import APIView

from sougou_weixin import sougou_weixin


class ConfigurationView(APIView):
    def get(self, request):

        response = {
            'code': 1,
            'data': '2',
        }
        return Response(response)