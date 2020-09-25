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
        return get_random_string(length=64)

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
    # Stores the raw password if set_password() is called so that it can
    # be passed to password_changed() after the model is saved.
    _password = None




    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

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

    def clean(self):
        super().clean()
        self.email = self.normalize_email(self.email)

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
        self.set_password(self.password)
        self.email = self.normalize_email(self.email)
        self.send_verification_email(self.email)
        super(Student, self).save(*args, **kwargs)
