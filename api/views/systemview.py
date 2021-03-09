from rest_framework.response import Response
from rest_framework.views import APIView

from sougou_weixin.sougou_weixin import run_weixin_crawler


class StartWeinxinView(APIView):
    def get(self, request):
        run_weixin_crawler()
        response = {
            'code': 1,
            'data': 'started!',
        }
        return Response(response)