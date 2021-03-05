from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import TargetSerializer
from api.models import Target


class TargetView(APIView):
    # 新增
    def post(self, request):
        serializer = TargetSerializer(data=request.data)
        if serializer.is_valid():
            if not Target.objects.filter(target=request.data['target'], center_id=request.data['center_id']):
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
    # 获取全部target
    def get(self, request):
        target = Target.objects.all()
        serializer = TargetSerializer(target, many=True)
        response = {
            'code': 1,
            'data': serializer.data,
        }
        return Response(response)

    # 分页获取全部target
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
    # 选择中心，获取中心下的target
    # 获取对应id的target
    def post(self, request):
        if 'id' in request.data.keys():
            id = request.data['id']
            target = Target.objects.get(id=id)
            serializer = TargetSerializer(target)
        elif 'center_id' in request.data.keys():
            center_id = request.data['center_id']
            target = Target.objects.filter(center_id=center_id)
            serializer = TargetSerializer(target, many=True)
        else:
            response = {
                'code': 0,
                'data': ['id or center_id is required'],
            }
            return Response(response)

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
        count = Target.objects.filter(target=request.data['target'], center_id=request.data['center_id']).exclude(id=uid).count()
        if count > 0 :
            response = {
                'code': 0,
                'message': 'Target 已存在',
            }
            return Response(response)
        else:
            try:
                target = Target.objects.get(id=uid)
            except:
                response = {
                    'code': 0,
                    'message': 'id不存在',
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

