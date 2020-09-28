import datetime
from django.utils.timezone import utc
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.conf import settings

EXPIRE_HOURS = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_HOURS', 1)

class ExpiringTokenAuthentication(TokenAuthentication):
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

        return token.user, token
