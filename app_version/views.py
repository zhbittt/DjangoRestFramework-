from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.versioning import QueryParameterVersioning


class UserInfo(APIView):
    '''
    基于url的get传参方式 / appversion?version = v1
    '''
    # versioning_class = QueryParameterVersioning
    def get(self,requset):
        ret = {'info':"示例"}
        #
        # ver = requset.query_params.get('version')
        # print(ver)
        # if ver == 'v1':
        #     ret['info']='版本v1'
        # elif ver == 'v2':
        #     ret['info']='版本v2'
        # else:
        #     ret['info']='不支持版本%s'%ver
        ver1 = requset.version
        ver2 = requset.versioning_scheme
        print(ver1,ver2)

        revers_url = requset.versioning_scheme.reverse('vuser',request=requset)
        print(revers_url) #http://127.0.0.1:8000/appversion/v2/index/
        return Response(ret)


class IndexView(APIView):
    '''
    基于url的正则方式 如：/v1/index/
    '''
    def get(self,request,version):
        ver1 = request.version
        ver2 = request.versioning_scheme
        print(ver1,ver2,version)
        self.dispatch
        revers_url = request.versioning_scheme.reverse('vindex', request=request)
        print(revers_url)
        return Response(ver1)
