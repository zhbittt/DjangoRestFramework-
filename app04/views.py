from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from app01 import models
from rest_framework import exceptions
from rest_framework.throttling import BaseThrottle,SimpleRateThrottle
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
import time
from rest_framework.exceptions import APIException

#====================================================================认证
class MyAuthentication(BaseAuthentication):
    def authenticate(self,request):
        user = request.query_params.get('user',None)
        if user:
            obj = models.UserInfo.objects.filter(username=user).first()
            return (user,obj)
        # return None
        raise exceptions.AuthenticationFailed('认证失败了')

#====================================================================权限

class MyPermission(BasePermission):
    message='没有权限访问11111'
    def has_permission(self, request, view):
        if request.user:
            return True
        raise APIException('323')



#====================================================================限制访问频率
class AnonSimpleRateThrottle(SimpleRateThrottle):
    '''
    匿名和注册用户都能访问
    '''
    scope = 'myscope_anon'
    def get_cache_key(self, request, view):
        # 登录用户我不管
        if request.user:
            return None
        # 匿名用户
        return self.get_ident(request)

class UserSimpleRateThrottle(SimpleRateThrottle):
    '''
    注册用户才能访问
    '''
    scope = 'myscope_user'
    def get_cache_key(self, request, view):
        # 登录用户
        if request.user:
            return request.user
        # 匿名用户我不管
        return None

class IndexView(APIView):
    authentication_classes = [MyAuthentication,]
    permission_classes = []
    throttle_classes = [AnonSimpleRateThrottle,UserSimpleRateThrottle]
    def get(self,request):
        # self.dispatch
        return Response({'info':'查看主页'})

    # def throttled(self, request, wait):
    #     class MyThrottled(exceptions.Throttled):
    #         '''
    #         自定义类，是为了访问超出限制后，给提提示中文的信息
    #         '''
    #         default_detail = '访问次数过于频繁'
    #         extra_detail_singular = 'Expected available in {wait} second.'
    #         extra_detail_plural = '还剩 {wait} 秒可再次访问'
    #     raise MyThrottled(wait)

class AdminView(APIView):
    authentication_classes = [MyAuthentication,]
    permission_classes = [MyPermission,]
    throttle_classes = [AnonSimpleRateThrottle,UserSimpleRateThrottle]
    def get(self,request):
        self.dispatch
        return Response({'info':'管理员页面'})

    # def throttled(self, request, wait):
    #     class MyThrottled(exceptions.Throttled):
    #         '''
    #         自定义类，是为了访问超出限制后，给提提示中文的信息
    #         '''
    #         default_detail = '访问次数过于频繁'
    #         extra_detail_singular = 'Expected available in {wait} second.'
    #         extra_detail_plural = '还剩 {wait} 秒可再次访问'
    #     # raise MyThrottled(wait)