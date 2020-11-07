from django.urls import path, re_path
from . import views
from rest_framework.authtoken import views as authviews
from django_encrypted_filefield.constants import FETCH_URL_NAME

FETCH_URL_NAME = FETCH_URL_NAME[FETCH_URL_NAME.find(':')+1:] # delete namespace from url
app_name = 'virtualclass'

urlpatterns = [
    path('', views.CustomAuthToken.as_view(), name='student_list'),
    path(r'get/<str:username>/', views.StudentDetailApiView.as_view(), name='detail'),
    path('create/', views.RegisterationApiView.as_view(), name='signup'),
    path('verify-email/', views.EmailVerification.as_view(), name="verify-email"),
    path('login/', views.LoginApiView.as_view(), name='login'),
    path(r'video/<str:title>/', views.DownloadVideoApiView.as_view(), name='download_video'),
    path('videos/', views.ListVideosApiView.as_view(), name='list_videos'),
    path('quizzes/', views.ListQuizzesApiView.as_view(), name='list_quizzes'),
    path('get-quiz/<str:title>/', views.getQuizApiView.as_view(), name='get_quiz'),
    path('submit-quiz/', views.submitQuizApiView.as_view(), name='submit_quiz'),
    re_path(
        r'^fetch/(?P<path>.+)/$',  # up to you, but path is required
        views.FetchVideoView.as_view(),          # your view, your permissions
        name=FETCH_URL_NAME
    ),
]
