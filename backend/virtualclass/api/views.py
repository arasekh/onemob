from rest_framework import generics
from virtualclass.models import Student
from .serializers import StudentListSerializer, StudentDetailSerializer, StudentCreateSerializer, EmailVerificationSerializer
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404

class StudentListApiView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentListSerializer

class StudentDetailApiView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentDetailSerializer
    lookup_field = 'id'

class StudentCreateApiView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentCreateSerializer
    permission_classes = [IsAdminUser]

class EmailVerification(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = EmailVerificationSerializer
    lookup_field = 'key'
