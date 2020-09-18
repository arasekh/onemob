from rest_framework.serializers import ModelSerializer
from virtualclass.models import Student

class PostListSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class PostDetailSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
