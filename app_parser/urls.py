
from django.conf.urls import url

from app_parser import views

urlpatterns = [
    url(r'^index/',views.IndexView.as_view(),name='pindex'),


]
