from rest_framework.serializers import ModelSerializer
from virtualclass.models import Student

class StudentListSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class StudentDetailSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class StudentCreateSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class EmailVerificationSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
