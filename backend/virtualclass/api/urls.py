from django.urls import path, re_path
from . import views
from rest_framework.authtoken import views as authviews

app_name = 'virtualclass'

urlpatterns = [
    path('', views.CustomAuthToken.as_view(), name='student_list'),
    path(r'get/<str:username>/', views.StudentDetailApiView.as_view(), name='detail'),
    path('create/', views.RegisterationApiView.as_view(), name='signup'),
    path(r'verify-email/<int:verification_key>/', views.EmailVerification.as_view(), name="verify-email"),
    path('login/', views.LoginApiView.as_view(), name='login')
]
