from rest_framework import generics
from virtualclass.models import Student, Video
from .serializers import StudentListSerializer, StudentDetailSerializer, RegisterationSerializer, EmailVerificationSerializer, StudentVideosSerializer
from django.shortcuts import get_object_or_404
from virtualclass.authentication import ExpiringTokenAuthentication
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.views import ObtainAuthToken
from django.shortcuts import get_object_or_404
from django.conf import settings
import datetime
from django.utils.timezone import utc
from django.http import HttpResponse, Http404
import os
from django.contrib.auth.mixins import AccessMixin
from django_encrypted_filefield.views import FetchView
from django.urls import reverse, NoReverseMatch
from django_encrypted_filefield.constants import FETCH_URL_NAME
from django_encrypted_filefield.crypt import Cryptographer
from django.shortcuts import redirect
import magic

EXPIRE_HOURS = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_HOURS', 1)

class CustomAuthToken(ObtainAuthToken):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Student.objects.all()
    serializer_class = StudentListSerializer
    def post(self, request, *args, **kwargs):
        student = request.auth.user
        return Response({
            'username': student.username,
            'email': student.email,
            'first_name': student.first_name,
            'last_name': student.last_name,
        })

class StudentListApiView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentListSerializer

class StudentDetailApiView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentDetailSerializer
    lookup_field = 'username'

class RegisterationApiView(generics.CreateAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Student.objects.all()
    serializer_class = RegisterationSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        student = serializer.save()
        student.send_verification_email()
        return Response({
            'response': 'successfully registered a new user',
            'username': student.username,
            'email': student.email,
        })

class LoginApiView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Student.objects.all()
    serializer_class = StudentDetailSerializer
    lookup_field = 'username'
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        student = get_object_or_404(Student, username=username)
        password1 = student.password
        password2 = request.data['password']
        if password1 != password2:
            raise ValidationError({'detail' : "Wrong Password"})
        token, created =  Token.objects.get_or_create(user=student)
        utc_now = datetime.datetime.utcnow().replace(tzinfo=utc)
        if not created:
            # delete previously created token if it is expired
            if token.created < utc_now - datetime.timedelta(hours=EXPIRE_HOURS):
                token.delete()
                token = Token.objects.create(user=student)
            # update the created time of the token to keep it valid
            token.created = datetime.datetime.utcnow()
            token.save()
        return Response({
            'email': student.email,
            'token': token.key,
            'email_valid': student.email_valid,
        })

class FetchVideoView(FetchView):
    def get(self, request, *args, **kwargs):
        path = kwargs.get("path")
        # No path?  You're boned.  Move along.
        if not path:
            raise Http404
        if path[0] != '/':
            path = '/' + path
        if self._is_url(path):
            content = requests.get(path, stream=True).raw.read()
        else:
            # Normalise the path to strip out naughty attempts
            path = path.replace(settings.MEDIA_URL, settings.MEDIA_ROOT, 1)
            path = os.path.normpath(path)
            # Evil path request!
            # if not path.startswith(settings.MEDIA_ROOT):
            #     raise Http404

            # The file requested doesn't exist locally.  A legit 404
            if not os.path.exists(path):
                raise Http404

            with open(path, "rb") as f:
                content = f.read()

        content = Cryptographer.decrypted(content)
        return HttpResponse(
            content, content_type=magic.Magic(mime=True).from_buffer(content))

class DownloadVideoApiView(APIView):
    queryset = Video.objects.all()
    def get(self, request, *args, **kwargs):
        title = kwargs.get("title")
        video = get_object_or_404(Video, title=title)
        MEDIA_URL = settings.MEDIA_URL
        if MEDIA_URL[0] == '/':
            MEDIA_URL = MEDIA_URL[1:]
        file_path = os.path.join(MEDIA_URL, video.video_file.name)
        try:
            return redirect(reverse(FETCH_URL_NAME, kwargs={"path": file_path}))
        except NoReverseMatch:
            return [Error(
                "There is no url to handle fetching local files!"
            )]
        return Http404

class ListVideosApiView(ObtainAuthToken):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        student = request.auth.user.student
        videos = student.videos.all()
        videos = [{'title': video.title, 'name': video.filename} for video in videos]

        return Response({
            'response': 'successfully got the videos',
            'username': student.username,
            'videos': videos,
        })

class EmailVerification(ObtainAuthToken):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        student = request.auth.user.student
        if request.data['verification_key'] != student.verification_key:
            raise ValidationError({'detail': 'verification_key provided is incorrect'})
        student.email_valid = True
        student.save()
        return Response({
            'response': 'successfully verified the email',
            'username': student.username,
            'email': student.email,
        })
    

class StudentLoginView(APIView):
    queryset = Student.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)
