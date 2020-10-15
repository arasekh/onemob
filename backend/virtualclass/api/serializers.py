from rest_framework.serializers import ModelSerializer
from virtualclass.models import Student, Video
from rest_framework import serializers

class StudentListSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class StudentDetailSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class StudentVideosSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ['videos']

class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = ['title']

class RegisterationSerializer(ModelSerializer):
    videos = VideoSerializer(read_only=True, required=False, many=True)
    class Meta:
        model = Student
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

class EmailVerificationSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
