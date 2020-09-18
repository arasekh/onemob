from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.PostListApiView.as_view(), name='post_list'),
    re_path(r'^(?P<id>[0-9]{1,3})/$', views.PostDetailApiView.as_view(), name='detail'),
    path('create/', views.PostCreateApiView.as_view(), name='create'),
]
