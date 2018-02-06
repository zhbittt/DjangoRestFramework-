from django.shortcuts import render


# IndexView
# UserView
# SalaryView
#使用全局
#认证+权限
#没有权限打印自定义的信息
#用户保存到数据库
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from rest_framework.authentication import BaseAuthentication
from app01 import models
from rest_framework import exceptions
class AllAuthentication(BaseAuthentication):
    def authenticate(self,request):
        user = request.query_params.get('user')
        obj = models.UserInfo.objects.filter(username=user).first()
        if user:
            return (user,obj)
        return None
    def authenticate_header(self, request):
        # return '用户认证失败'
        pass

class MyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user:
            return True
        raise exceptions.PermissionDenied(detail='你没有权限访问')

class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user=='alex':
            return True
        raise exceptions.PermissionDenied(detail='你没有权限访问')





class IndexView(APIView):
    authentication_classes = [AllAuthentication,]
    permission_classes = []
    def get(self,request):
        self.dispatch
        return Response({'info':'匿名和注册用户都能访问'})

class UserView(APIView):
    authentication_classes = [AllAuthentication,]
    permission_classes = [MyPermission]
    def get(self,request):
        return Response({'info':'注册用户才能访问'})

class SalaryView(APIView):
    authentication_classes = [AllAuthentication]
    permission_classes = [MyPermission,UserPermission]
    def get(self,request):
        return Response({'info':'alex的用户才能访问'})