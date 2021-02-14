from django.conf.urls import url, include
#from django.urls import path
from . import views

urlpatterns = [
    # /rev/
    url(r'^$', views.index, name='index'),
    url(r'aboutus', views.aboutus, name='aboutus'),
    url(r'upload', views.upload, name='upload'),
    url(r'estimation/(?:(?P<model_name>[\w\-\ \.]+)/)?$', views.estimation, name='estimation'),
    url(r'photos', views.photos, name='photos'),
    url(r'log_in', views.login, name='login'),
    url(r'log_out', views.log_out, name='logout'),
    url(r'signup', views.signup, name='signup'),
    ]
