from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.StudentListApiView.as_view(), name='student_list'),
    path(r'get/<str:username>/', views.StudentDetailApiView.as_view(), name='detail'),
    path('create/', views.StudentCreateApiView.as_view(), name='create'),
    path(r'verify-email/<int:key>/', views.EmailVerification.as_view(), name="verify-email"),
]
