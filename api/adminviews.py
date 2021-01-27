from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import TargetSerializer
from api.models import Target


class LoginView(APIView):
    def post(self, request):
        response = {
            'code': 1,
            'data': {"token": "admin-token"},
        }
        return Response(response)


class AdminInfoView(APIView):
    def get(self, request):
        response = {
            'code': 1,
            'data': {"roles": ["admin"], "introduction": "I am a super administrator",
                     "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
                     "name": "Super Admin"}
        }
        return Response(response)
