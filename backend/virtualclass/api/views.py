from rest_framework import generics
from virtualclass.models import Student
from .serializers import StudentListSerializer, StudentDetailSerializer, RegisterationSerializer, EmailVerificationSerializer
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
        })

class EmailVerification(ObtainAuthToken):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        student = request.auth.user.student
        if request.data['verification_key'] != student.verification_key:
            raise ValidationError({'detail': 'verification_key provided is incorrect'})
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
