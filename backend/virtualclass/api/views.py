from rest_framework import generics
from virtualclass.models import Student, Video, Quiz, QuizInfo, Question, Answer
from .serializers import (StudentListSerializer, StudentDetailSerializer, RegisterationSerializer, 
                            EmailVerificationSerializer, StudentVideosSerializer)
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
from django.http import HttpResponse, Http404, HttpResponseForbidden
import os
from django.contrib.auth.mixins import AccessMixin
from django_encrypted_filefield.views import FetchView
from django.urls import reverse, NoReverseMatch
from django_encrypted_filefield.constants import FETCH_URL_NAME
from django_encrypted_filefield.crypt import Cryptographer
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
import magic
from django.utils import timezone
import pytz
from django.core import serializers
import json

EXPIRE_HOURS = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_HOURS', 1)
EMAIL_SENT_TIMEOUT = getattr(settings, 'EMAIL_SENT_TIMEOUT', 1)

def create_token(student):
    token, created =  Token.objects.get_or_create(user=student)
    utc_now = timezone.now()
    if not created:
        # delete previously created token if it is expired
        if token.created < utc_now - timezone.timedelta(hours=EXPIRE_HOURS):
            token.delete()
            token = Token.objects.create(user=student)
        # update the created time of the token to keep it valid
        token.created = timezone.now()
        token.save()
    return token

# important Note: This method is called only after login and with a valid token
# so when this method is called, the callee must have had a valid token   
def extend_token_after_login(student):
    token, created =  Token.objects.get_or_create(user=student)
    utc_now = timezone.now()
    if created or token.created < utc_now - timezone.timedelta(hours=EXPIRE_HOURS):
        # You are in an invalid state because you don't even have a token or your token is expired
        raise PermissionDenied()
    # update the created time of the token to keep it valid
    token.created = timezone.now()
    token.save()
    return token

def raiseErrorIfTimeoutPassed(student):
    utc_now = timezone.now()
    tolerance = 5 # this is because of delay
    timeout = EMAIL_SENT_TIMEOUT - tolerance
    if student.email_sent_time > utc_now - timezone.timedelta(seconds=timeout):
        # You are in an invalid state because you can't receive an email while your timeout has not reached!
        raise ValidationError({'detail' : 'Sorry, We cannot send you an email within less than a minute!'})

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
        token = create_token(student)
        return Response({
            'response': 'successfully registered a new user',
            'username': student.username,
            'token': token.key,
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
        token = create_token(student)
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

class DownloadVideoApiView(ObtainAuthToken):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        title = kwargs.get("title")
        video = get_object_or_404(Video, title=title)
        student = request.auth.user
        # extend the student token because he/she is active
        extend_token_after_login(student)
        student_videos = student.videos.all()
        if video in student_videos:
            video_path = video.video_file.path
            with open(video_path, "rb") as f:
                content = f.read()
            content = Cryptographer.decrypted(content)
            return HttpResponse(
                content, content_type=magic.Magic(mime=True).from_buffer(content))
            # MEDIA_URL = settings.MEDIA_URL
            # if MEDIA_URL[0] == '/':
            #     MEDIA_URL = MEDIA_URL[1:]
            # file_uri = os.path.join(MEDIA_URL, video.video_file.name)
            # try:
            #     return redirect(reverse(FETCH_URL_NAME, kwargs={"path": file_uri}))
            # except NoReverseMatch:
            #     return [Error(
            #         "There is no url to handle fetching local files!"
            #     )]
            # return Http404
        else:
            raise PermissionDenied()

class ListVideosApiView(ObtainAuthToken):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        student = request.auth.user
        # extend the student token because he/she is active
        extend_token_after_login(student)
        videos = student.videos.all()
        videos = [{'title': video.title, 'name': video.filename} for video in videos]

        return Response({
            'response': 'successfully got the videos',
            'username': student.username,
            'videos': videos,
        })

class ListQuizzesApiView(ObtainAuthToken):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        student = request.auth.user
        # extend the student token because he/she is active
        extend_token_after_login(student)
        quizzes = student.quizzes.all()
        quiz_titles = [quiz.title for quiz in quizzes]

        return Response({
            'response': 'successfully got the quizzes',
            'username': student.username,
            'quiz_titles': quiz_titles,
        })

class getQuizApiView(ObtainAuthToken):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        title = kwargs.get("title")
        quiz = get_object_or_404(Quiz, title=title)
        quiz_id = quiz.id
        student = request.auth.user
        # extend the student token because he/she is active
        extend_token_after_login(student)
        student_quizzes = student.quizzes.all()
        if quiz in student_quizzes:
            questions_query_set = quiz.get_questions()
            quiz = []
            for question_query in questions_query_set:
                question = {'id': question_query.id, 'text': question_query.prompt}
                answers = []
                for answer_query in question_query.get_answers():
                    answers += [{'id': answer_query.id, 'text': answer_query.text, 'correct': answer_query.correct}]
                quiz += [{'question': question, 'answers': answers}]
            return Response({
                'response': 'successfully got the quiz',
                'username': student.username,
                'quiz_id': quiz_id,
                'quiz_title': title,
                'quiz': quiz,
            })
        else:
            raise PermissionDenied()

class submitQuizApiView(ObtainAuthToken):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        student = request.auth.user
        # extend the student token because he/she is active
        extend_token_after_login(student)
        quiz_id = request.data['quiz_id']
        quiz_answers = json.loads(request.data['quiz_answers'])
        quiz = get_object_or_404(Quiz, id=quiz_id)
        student_quizzes = student.quizzes.all()
        score = 0
        if quiz in student_quizzes:
            quiz_questions = quiz.get_questions()
            for answer in quiz_answers:
                question_id = answer['question_id']
                answer_id = answer['answer_id']
                try:
                    # question = get_object_or_404(Question, id=question_id)
                    question = Question.objects.get(id=question_id)
                    if question not in quiz_questions:
                        raise Exception()
                except:
                    raise ValidationError({'detail': 'question ids provided are incorrect'})
                quiz_answers = question.get_answers()
                try:
                    # answer = get_object_or_404(Answer, id=answer_id)
                    answer = Answer.objects.get(id=answer_id)
                    if answer not in quiz_answers:
                        raise Exception()
                except:
                    raise ValidationError({'detail': 'answer ids provided are incorrect'})
                if answer.correct:
                    score += 1
            quizInfo = QuizInfo.objects.create(quiz=quiz, student=student, score=score)
            return Response({
                'response': 'successfully submitted the quiz',
                'username': student.username,
                'score': score,
            })
        else:
            raise PermissionDenied()
    
class EmailVerification(ObtainAuthToken):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        student = request.auth.user
        # extend the student token because he/she is active
        extend_token_after_login(student)
        if request.data['verification_key'] != student.verification_key:
            raise ValidationError({'detail': 'verification_key provided is incorrect'})
        student.email_valid = True
        student.save()
        return Response({
            'response': 'successfully verified the email',
            'username': student.username,
            'email': student.email,
        })
    
class EmailResend(ObtainAuthToken):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        student = request.auth.user
        # extend the student token because he/she is active
        extend_token_after_login(student)
        raiseErrorIfTimeoutPassed(student)
        # change the verification token for security reasons
        student.update_verification_token()
        student.send_verification_email()
        return Response({
            'response': 'successfully resent the email',
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