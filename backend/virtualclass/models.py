from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import forms
from django.utils import timezone
from email_utils import send_email
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .storages import getLocalVideoStorage, getRemoteVideoStorage
from django.conf import settings
import ffmpeg_streaming
from ffmpeg_streaming import Formats
from threading import Thread
from time import sleep
import os
from django_encrypted_filefield.fields import EncryptedFileField
import ffmpeg


def select_storage():
    return getLocalVideoStorage() if settings.DEBUG else MyRemoteStorage()

def compress_video_file(input_file_name):
    input_file = str(settings.MEDIA_ROOT + input_file_name)
    # output_file = str(path_root + output_file_name)
    stream = ffmpeg.input(input_file)
    stream = ffmpeg.output(stream,  str(settings.MEDIA_ROOT + 'out.mp4'), crf=28, vcodec='libx265')
    ffmpeg.run(stream)

def convert_video_to_hls(arg):
    path_root = settings.MEDIA_ROOT + arg.title
    if not os.path.exists(path_root):
        os.makedirs(path_root)
    video = ffmpeg_streaming.input(str(settings.MEDIA_ROOT + arg.video_file.name))
    save_to = str(path_root + '/key')
    #A URL (or a path) to access the key on your website
    url = settings.MEDIA_URL + arg.title + '/key'
    # or url = '/"PATH TO THE KEY DIRECTORY"/key';

    hls = video.hls(Formats.h264())
    hls.encryption(save_to, url)
    hls.auto_generate_representations()
    hls.output(str(path_root + '/hls.m3u8'))

class Video(models.Model):
    title = models.CharField(max_length=50)
    video_file = EncryptedFileField(upload_to='videos/', blank=True)

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

class Student(User):
    email_valid = models.BooleanField(
        default=False,
        verbose_name=_("has valid email"),
    )
    videos = models.ManyToManyField(Video)
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
        verbose_name_plural = _("Student")
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

    def save(self, *args, **kwargs):
        self.last_login = timezone.now()
        self.email = self.normalize_email(self.email)
        super(Student, self).save(*args, **kwargs)

# @receiver(post_save, sender='virtualclass.Student')
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)