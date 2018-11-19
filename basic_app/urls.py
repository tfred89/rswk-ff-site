from django.conf.urls import url
from django.urls import path, re_path
from basic_app import views

app_name = 'basic_app'

urlpatterns = [
    re_path(r'^seasonstats/$', views.season, name='season'),
    re_path('', views.home, name='home'),
    # re_path(r'^pastseasons/$', views.past, name='past'),
]
