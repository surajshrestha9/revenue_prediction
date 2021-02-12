from django.conf.urls import url, include
#from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    # /rev/
    url(r'^$', views.index, name='index'),
    url(r'aboutus', views.aboutus, name='aboutus'),
    url(r'upload', views.upload, name='upload'),
    url(r'estimation/(?:(?P<model_name>[\w\-\ \.]+)/)?$', views.estimation, name='estimation'),
    url(r'photos', views.photos, name='photos'),
    ]
