# from django.conf.urls import url
from django.conf.urls import url
from django.urls import path, re_path
from . import views


app_name = 'store'
urlpatterns = [
    path('', views.listing, name="listing"),
    # url(r'^(?P<album_id>[0-9]+)/$', views.detail),
    re_path(r'^(?P<album_id>[0-9]+)/$', views.detail, name="detail"),
    path('search/', views.search, name="search"),
]
