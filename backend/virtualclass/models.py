from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import forms
from django.utils import timezone
from email_utils import send_email
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

class Student(models.Model):
    def generate_token():
        """
        Get a random 64 character string.
        Returns:
            str:
                A random 64 character string.
        """
        return get_random_string(length=6, allowed_chars='0123456789')

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField()
    password = models.CharField(_('password'), max_length=128)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    key = models.CharField(
        default=generate_token,
        editable=False,
        max_length=255,
        verbose_name="confirmation key",
    )

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
            "verification_token": self.key
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
