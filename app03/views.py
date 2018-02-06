from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from app01 import models
from rest_framework import exceptions
from rest_framework.throttling import BaseThrottle,SimpleRateThrottle
import time
from rest_framework.exceptions import APIException


RECORD = {}
class MyThrottle(BaseThrottle):
    '''
    仿照SimpleRateThrottle这个类，做简单化处理，看懂后在看SimpleRateThrottle就很简单了
    '''
    scope = 'mythrottle' # 在配置文件里需要有个跟这个同名
    def allow_request(self, request, view):
        """
        # 返回False，限制
        # 返回True，通行
        :param request:
        :param view:
        :return:
        """
        """
         a. 对匿名用户进行限制：每个用户1分钟允许访问10次
            - 获取用户IP request 1.1.1.1
        """
        ctime =time.time()
        IP = self.get_ident(request)
        if IP not in RECORD:
            RECORD[IP] = [ctime]
        else:
            throttle_list=RECORD[IP]
            while True:
                val=0
                if len(throttle_list):
                    val = throttle_list[-1]
                if ctime - val>60:
                    throttle_list.pop()
                else:
                    break
            if len(throttle_list) > 3:
                return False
            RECORD[IP].insert(0,ctime)
        return True

    def wait(self):
        # ctime = time.time()
        # first_in_time = RECORD[self.get_ident()][-1]
        # rw = 60 - (ctime - first_in_time)
        return 2


# class MySimpleRateThrottle(SimpleRateThrottle):
#     scope = 'myscope_anon'
#     def get_cache_key(self, request, view):
#         return self.get_ident(request)
# class LimitView(APIView):
#     authentication_classes = []
#     permission_classes = []
#     throttle_classes = [MySimpleRateThrottle, ]
#     # throttle_classes = [MyThrottle,]
#     def get(self,request):
#         self.dispatch
#         return Response({'info':'控制访问频率示例',})
#
#     def throttled(self, request, wait):
#         class MyThrottled(exceptions.Throttled):
#             default_detail ='请求被限制.'
#             extra_detail_singular = 'Expected available in {wait} second.'
#             extra_detail_plural = '还需要再等待{wait}'
#
#         raise MyThrottled(wait)


class MySimpleRateThrottle(SimpleRateThrottle):
    scope = 'myscope_anon'
    def get_cache_key(self, request, view):
        return self.get_ident(request)

class LimitView(APIView):
    throttle_classes = [MySimpleRateThrottle,]
    def get(self,request):
        # self.dispatch
        return Response({'info':'限制访问频率示例'})

    def throttled(self, request, wait):
        class MyThrottled(exceptions.Throttled):
            '''
            自定义类，是为了访问超出限制后，给提提示中文的信息
            '''
            default_detail = '访问次数过于频繁'
            extra_detail_singular = 'Expected available in {wait} second.'
            extra_detail_plural = '还剩 {wait} 秒可再次访问'
        raise MyThrottled(wait)
