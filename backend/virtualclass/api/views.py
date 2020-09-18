from rest_framework import generics
from virtualclass.models import Student
from .serializers import PostListSerializer, PostDetailSerializer
from rest_framework.permissions import IsAdminUser

class PostListApiView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = PostListSerializer

class PostDetailApiView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = PostListSerializer
    lookup_field = 'id'

class PostCreateApiView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [IsAdminUser]
