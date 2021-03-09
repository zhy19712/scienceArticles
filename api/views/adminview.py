import time

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import TargetSerializer, UserSerializer
from api.models import Target, User
from api.util import make_password


class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        password = make_password(password)
        token = make_password(str(time.time()))

        try:
            user = User.objects.get(username=username, status=0)
        except ObjectDoesNotExist:
            try:
                user = User.objects.get(username=username, password=password)
            except ObjectDoesNotExist:
                response = {
                    'code': 0,
                    'message': '用户名或密码不正确'
                }
                return Response(response)
            else:
                data = {
                    'token': token
                }
                serializer = UserSerializer(data=data, instance=user)
                if serializer.is_valid():
                    serializer.save()
                    response = {
                        'code': 1,
                        'data': {"token": token}
                    }
                    return Response(response)
                else:
                    return Response(serializer.errors)
        else:
            response = {
                'code': 0,
                'message': '用户被封禁，请联系管理员'
            }
            return Response(response)

    def get(self, request):
        response = {
            'code': 1,
            'message': 'user logged out'
        }
        return Response(response)


class AdminInfoView(APIView):
    def post(self, request):
        token = request.data['token']
        try:
            user = User.objects.get(token=token)
            serializer = UserSerializer(user)
        except:
            response = {
                'code': 0,
                'message': '用户信息失效，请重新登录！'
            }
            return Response(response)
        else:
            response = {
                'code': 1,
                'data': {"roles": ["admin"], "introduction": "I am a super administrator",
                         "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
                         "name": serializer.data['username'],
                         "center_id": serializer.data['center_id'],
                         "id": serializer.data['id']
                         },
            }
            return Response(response)


class UserView(APIView):
    # 创建一个用户，默认密码为123
    def post(self, request):
        username = request.data['username']
        center_id = request.data['center_id']

        if User.objects.filter(username=username).count() == 0:
            password = make_password('123')
            data = {
                'username': username,
                'password': password,
                'center_id': center_id,
                'status': 1
            }
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'code': 1,
                    'data': serializer.data,
                }
                return Response(response)
            else:
                return Response(serializer.errors)
        else:
            response = {
                'code': 0,
                'message': '用户名已存在'
            }
            return Response(response)

    # 重置用户密码
    def put(self, request):
        uid = request.data['id']
        data = {
            'id': uid,
            'password': make_password("123")
        }
        try:
            user = User.objects.get(id=uid)
        except:
            response = {
                'code': 0,
                'message': '用户id不存在',
            }
            return Response(response)
        else:
            serializer = UserSerializer(data=data, instance=user)
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
            User.objects.get(id=uid).delete()
        except:
            response = {
                'code': 0,
                'message': '用户id不存在',
            }
            return Response(response)
        else:
            response = {
                'code': 1,
                'message': '删除成功',
            }
            return Response(response)


class UserFilterView(APIView):
    def post(self, request):
        if 'id' in request.data:
            uid = request.data['id']
            user = User.objects.get(id=uid)
            serializer = UserSerializer(user)
            response = {
                'code': 1,
                'data': serializer.data
            }
            return Response(response)
        elif 'center_id' in request.data:
            center_id = request.data['center_id']
            user = User.objects.filter(center_id=center_id)
            serializer = UserSerializer(user, many=True)
            response = {
                'code': 1,
                'data': serializer.data
            }
            return Response(response)

    def put(self, request):
        uid = request.data['id']
        password = make_password(request.data['password'])
        new_password = make_password(request.data['new_password'])
        data = {
            'id': uid,
            'password': new_password
        }
        try:
            user = User.objects.get(id=uid, password=password)
        except:
            response = {
                'code': 0,
                'message': '原密码错误',
            }
            return Response(response)
        else:
            serializer = UserSerializer(data=data, instance=user)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'code': 1,
                    'data': serializer.data,
                }
                return Response(response)
            else:
                return Response(serializer.errors)


class UserStatusView(APIView):
    def post(self, request):
        uid = request.data['id']
        status = request.data['status']
        data = {
            'id': uid,
            'status':status
        }
        try:
            user = User.objects.get(id=uid)
        except:
            response = {
                'code': 0,
                'message': '用户id不存在',
            }
            return Response(response)
        else:
            serializer = UserSerializer(data=data, instance=user)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'code': 1,
                    'data': serializer.data,
                }
                return Response(response)
            else:
                return Response(serializer.errors)
