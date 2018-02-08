
from django.conf.urls import url,include

from app_version import views

urlpatterns = [
    #版本
    #基于url的get传参方式  /appversion?version=v1
    url(r'^user/',views.UserInfo.as_view(),name='vuser'),
    #基于url的正则方式 如：/v1/users/
    url(r'^index/',views.IndexView.as_view(),name='vindex'),


]
