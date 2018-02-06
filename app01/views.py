from rest_framework.views import APIView
from django.shortcuts import HttpResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import APIException
from app01 import models

import hashlib
import time
import json
from rest_framework.permissions import AllowAny
from rest_framework.permissions import BasePermission
class MyAuthentication(BaseAuthentication):
    '''
    自定义用户认证，get方式，url？user=xxx&pwd=xxx
    从数据库查询用户是否注册，已注册用md5生成一段随机字段，交给请求者当做cookie，下次带着这个cookie来就行（防止账号密码泄露），
    '''
    def authenticate(self, request):
        user = request.query_params.get('user', None)
        pwd = request.query_params.get('pwd', None)
        obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
        if obj :
            ctime = time.time()
            msg= '%s|%s'%(obj.username,ctime)
            m = hashlib.md5()
            m.update(msg.encode('utf-8'))
            # token = m.digest()
            token=m.hexdigest() #16位编码

            #保存数据
            obj.token=token
            obj.save()
            return (obj.username,obj)
        raise APIException('用户认证失败')

class ALLAuthentication(BaseAuthentication):
    '''
    自定义用户认证，匿名用户，注册用户都可以访问
     def authenticate(self, request):
        有三种返回值
            None  当前不做处理，交给后面函数的做处理，如果都不处理，返回匿名名称（从配置文件UNAUTHENTICATED_USER找）
            （user，auth） 已经处理，结束认证，之后的认证都不处理了
            raise  出错
    '''
    def authenticate(self, request):
        user = request.query_params.get('user', None)
        obj = models.UserInfo.objects.filter(username=user).first()
        if obj:
            return (obj.username,obj)
        return None

class MyTokenAuthentication(BaseAuthentication):
    '''
    自定义用户认证,UserInfo表token字段能匹配上的可以访问
    '''
    def authenticate(self, request):
        token = request.query_params.get('token', None)
        obj = models.UserInfo.objects.filter(token=token).first()
        if obj:
            return (obj.username, obj)
        raise APIException('用户认证失败')

class MyPermission(BasePermission):
    '''
    def has_permission(self, request, view):
        两种结果
            true  有权访问，执行其他权限类
            false  最后也是执行raise 报错 ，所以 false 也可以用raise替换
    '''
    message = '无权访问'
    def has_permission(self, request, view):
        if request.user:
            return True
        return False

class TokenPermission(BasePermission):
    message = '无权访问'
    def has_permission(self, request, view):
        # print('has_permission',request._request.path,view.get_view_name())
        obj = models.UserInfo.objects.filter(token=request.user).first()
        if obj:
            return True
        return False

class AuthView(APIView):
    authentication_classes = [MyAuthentication,]
    def get(self, request):
        ret = {'code': None, 'info': None, 'token': None}
        ret['code']=1000
        ret['info']='登录成功'
        ret['token']=request.auth.token
        return Response({'info':'用户的登录认证'})

class IndesView(APIView):
    authentication_classes = [ALLAuthentication, ]
    permission_classes = []
    def get(self,request):
        print(self.request.user)
        return Response({'code':1000,'info':'index页面,谁都能访问'})

class UserView(APIView):
    authentication_classes = [ALLAuthentication, ]
    permission_classes = [MyPermission,]
    def get(self, request):
        print(self.request.user)
        # print(self.request.auth)
        msg = {'code': 200, 'is_login': True, 'user': request.user, 'token': request.auth.token,'info':'登录之后才能访问'}
        return Response(msg)

class SalaryView(APIView):

    authentication_classes = [ALLAuthentication, ]
    permission_classes = [MyPermission, ]
    def get(self, request):
        print(request.user)
        # self.dispatch
        ret = {'code': None, 'info': None, 'token': None}
        ret['code']=1000
        ret['info']='登录成功'
        ret['token']=request.auth.token
        return Response(ret)