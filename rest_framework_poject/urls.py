"""rest_framework_poject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
# from app01 import views
# from app02 import views as app02_views
# from app03 import views as app03_views
# from app04 import views as app04_views
from app_serializers import views as app_ser_views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^user/',views.UserView.as_view()),
    # url(r'^auth/',views.AuthView.as_view()),
    # url(r'^index/',views.IndesView.as_view()),
    # url(r'^salary/',views.SalaryView.as_view()),
    # url(r'^index/',app02_views.IndexView.as_view()),
    # url(r'^user/',app02_views.UserView.as_view()),
    # url(r'^salary/',app02_views.SalaryView.as_view()),
    # url(r'^index/',app04_views.IndexView.as_view()),
    # url(r'^adminn/',app04_views.AdminView.as_view()),

    #版本 version
    #基于url的get传参方式  /appversion?version=v1
    # url(r'^appversion/',include('app_version.urls')),
    #基于url的正则方式 如：/v1/index/
    # url(r'^appversion/(?P<version>[v1|v2]+)/', include('app_version.urls')),

    #解析器 parser
    # url(r'^appparser/', include('app_parser.urls')),

    # 序列化
    url(r'^suser/',app_ser_views.UsersView.as_view(),name='suser'),
    url(r'^index/',app_ser_views.IndexView.as_view()),
    url(r'^aa/',app_ser_views.AAView.as_view()),
    url(r'detail/(?P<pk>\d+)/', app_ser_views.AAView.as_view(), name='detail'),
]
