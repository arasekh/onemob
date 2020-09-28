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

class RegisterationSerializer(ModelSerializer):
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
