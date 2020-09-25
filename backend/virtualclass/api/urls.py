from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.StudentListApiView.as_view(), name='student_list'),
    re_path(r'^(?P<id>[0-9]{1,3})/$', views.StudentDetailApiView.as_view(), name='detail'),
    path('create/', views.StudentCreateApiView.as_view(), name='create'),
    path(r'verify-email/<str:key>/', views.EmailVerification.as_view(), name="verify-email"),
]
