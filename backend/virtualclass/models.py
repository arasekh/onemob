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

class Student(User):
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
        verbose_name="confirmation key",
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

    def send_verification_email(self, email):
        context = {
            "username": self.username,
            "verification_token": self.verification_key
        }
        send_email(
            context=context,
            from_email='no-reply@gmail.com',
            recipient_list=[email],
            subject='Please do not reply this message',
            template_name='virtualclass/email-verification',
        )

    def save(self, *args, **kwargs):
        self.last_login = timezone.now()
        self.email = self.normalize_email(self.email)
        self.send_verification_email(self.email)
        super(Student, self).save(*args, **kwargs)

# @receiver(post_save, sender='virtualclass.Student')
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
