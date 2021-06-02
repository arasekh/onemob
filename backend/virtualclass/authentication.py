import datetime
from django.utils.timezone import utc
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.core.exceptions import PermissionDenied

EXPIRE_HOURS = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_HOURS', 1)


class ExpiringTokenAuthentication(TokenAuthentication):

    keyword = settings.AUTH_HEADER_PREFIX

    # important Note: This method is called only after login and with a valid token
    # so when this method is called, the callee must have had a valid token
    def _extend_token(self, student):
        token, created = Token.objects.get_or_create(user=student)
        utc_now = timezone.now()
        if created or token.created < utc_now - timezone.timedelta(hours=EXPIRE_HOURS):
            # You are in an invalid state because you don't even have a token or your token
            # is expired
            raise PermissionDenied()
        # update the created time of the token to keep it valid
        token.created = timezone.now()
        token.save()
        return token

    def authenticate_credentials(self, key):
        try:
            self.model = self.get_model()
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        # if not token.user.is_active:
        #     raise exceptions.AuthenticationFailed('User inactive or deleted')

        # This is required for the time comparison
        utc_now = datetime.datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=utc)

        if token.created < utc_now - datetime.timedelta(hours=EXPIRE_HOURS):
            raise exceptions.AuthenticationFailed('Token has expired')

        self._extend_token(token.user)

        return token.user, token
