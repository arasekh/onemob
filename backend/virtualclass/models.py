from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# comment this to avoid errors concerning AUTH_USER_MODEL
# from django.contrib.auth import forms
from email_utils import send_email
from django.utils.crypto import get_random_string
from .storages import getLocalVideoStorage, getRemoteVideoStorage
from django.conf import settings
import ffmpeg_streaming
from ffmpeg_streaming import Formats
import os
from django_encrypted_filefield.fields import EncryptedFileField
import ffmpeg
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver


def select_storage():
    return getLocalVideoStorage() if settings.DEBUG else getRemoteVideoStorage()


def compress_video_file(input_file_name):
    input_file = str(settings.MEDIA_ROOT + input_file_name)
    # output_file = str(path_root + output_file_name)
    stream = ffmpeg.input(input_file)
    stream = ffmpeg.output(stream, str(settings.MEDIA_ROOT + 'out.mp4'), crf=28, vcodec='libx265')
    ffmpeg.run(stream)


def convert_video_to_hls(arg):
    path_root = settings.MEDIA_ROOT + arg.title
    if not os.path.exists(path_root):
        os.makedirs(path_root)
    video = ffmpeg_streaming.input(str(settings.MEDIA_ROOT + arg.video_file.name))
    save_to = str(path_root + '/key')
    # A URL (or a path) to access the key on your website
    url = settings.MEDIA_URL + arg.title + '/key'
    # or url = '/"PATH TO THE KEY DIRECTORY"/key';

    hls = video.hls(Formats.h264())
    hls.encryption(save_to, url)
    hls.auto_generate_representations()
    hls.output(str(path_root + '/hls.m3u8'))


class Video(models.Model):
    number = models.IntegerField(unique=True)
    title = models.CharField(max_length=50, unique=True)
    video_file = EncryptedFileField(upload_to=settings.VIDEO_FILES_UPLOAD_TO)
    price = models.DecimalField(max_digits=19, decimal_places=4)

    @property
    def filename(self):
        return os.path.basename(self.video_file.name)

    def save(self, *args, **kwargs):
        super(Video, self).save(*args, **kwargs)
        # compress_video_file(self.video_file.name)
        # thread = Thread(target = convert_video_to_hls, args = (self, ))
        # thread.start()

    def __str__(self):
        return self.title


class Quiz(models.Model):
    # author = models.ForeignKey(Student, on_delete=models.DO_NOTHING, default=None)
    title = models.CharField(max_length=255, default='')
    # created_at = models.DateTimeField(auto_now_add=True)
    # times_taken = models.IntegerField(default=0, editable=False)

    @property
    def question_count(self):
        return self.questions.count()

    def get_questions(self):
        return self.questions.all()

    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['id']

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        related_name='questions',
        on_delete=models.DO_NOTHING
    )
    prompt = models.CharField(max_length=255, default='')

    def get_answers(self):
        return self.answers.all()

    class Meta:
        verbose_name_plural = "Questions"
        ordering = ['id']

    def __str__(self):
        return self.prompt


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.DO_NOTHING
    )
    text = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Answers"

    def __str__(self):
        return self.text


class Student(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    email_valid = models.BooleanField(
        default=False,
        verbose_name=_("has valid email"),
    )
    email_sent_time = models.DateTimeField(blank=True, null=True)
    videos = models.ManyToManyField(Video, blank=True)
    quizzes = models.ManyToManyField(Quiz, blank=True, related_name='quizzes')
    quiz_info = models.ManyToManyField(Quiz, through='QuizInfo', blank=True,
                                       related_name='quiz_info')
    balance = models.DecimalField(max_digits=19, decimal_places=4, blank=False, null=False,
                                  default=1000, editable=False)

    def generate_token():
        """
        Get a random 64 character string.
        Returns:
            str:
                A random 64 character string.
        """
        return get_random_string(length=6, allowed_chars='0123456789')

    verification_key = models.CharField(
        default=generate_token,
        editable=False,
        max_length=255,
        verbose_name=_("confirmation key"),
    )

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")

    def __str__(self):
        return self.username

    def normalize_email(self, email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = email_name + '@' + domain_part.lower()
        return email

    def update_verification_token(self):
        self.verification_key = Student.generate_token()
        self.save()

    def send_verification_email(self):
        context = {
            "username": self.username,
            "verification_token": self.verification_key
        }
        send_email(
            context=context,
            from_email='no-reply@gmail.com',
            recipient_list=[self.email],
            subject='Please do not reply this message',
            template_name='virtualclass/email-verification',
        )
        self.email_sent_time = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        self.last_login = timezone.now()
        self.email = self.normalize_email(self.email)
        super(Student, self).save(*args, **kwargs)


class QuizInfo(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='students')
    score = models.IntegerField()


class Transaction(models.Model):
    # id created by the receiver of the transaction
    # order_id = models.CharField(max_length=50, verbose_name=_('order id'))

    user = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, related_name='user')
    # Unique id returned by the payment gateway for this transaction
    payment_id = models.TextField(unique=True, null=True, blank=True,
                                  verbose_name=_('payment id'))
    payment_link = models.TextField(verbose_name=_('payment link'))
    idpay_track_id = models.IntegerField(unique=True, null=True, blank=True)
    bank_track_id = models.TextField(unique=True, null=True, blank=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2, verbose_name=_('amount'))
    card_number = models.TextField(default="****", verbose_name=_('card number'))
    hashed_card_number = models.TextField(null=True, blank=True,
                                          verbose_name=_('hashed card number'))
    date = models.DateTimeField(default=timezone.now)

    class TransactionStatus(models.IntegerChoices):
        # Refer to https://idpay.ir/web-service/v1.1/#ad39f18522 for more details about
        # status codes!
        incomplete = 1
        unsuccessful = 2
        error = 3
        blocked = 4
        payerRedirect = 5
        systemRedirect = 6
        cancelled = 7
        gatewayRedirect = 8
        verificationPending = 10
        verified = 100
        alreadyVerified = 101
        received = 200

    status = models.IntegerField(choices=TransactionStatus.choices,
                                 default=TransactionStatus.incomplete)

    def __str__(self):
        return str(self.pk) + " " + self.get_status_display()

# @receiver(post_save, sender='virtualclass.Student')
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


@receiver(post_delete, sender=Video)
def delete_video_file(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.video_file.delete(False)
