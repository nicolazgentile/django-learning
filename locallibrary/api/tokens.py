from rest_framework.authtoken.models import Token

from datetime import timedelta, datetime
from django.utils import timezone
from django.conf import settings


#this return left time
def expires_in(token):
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    return left_time

# token checker if token expired or not
def is_token_expired(token):
    return expires_in(token) < timedelta(seconds = 0)

# if token is expired new token will be established
# If token is expired then it will be removed
# and new one with different key will be created
def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = Token.objects.create(user=token.user)
    return is_expired, token





from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed


# class ExpiringTokenAuthentication(TokenAuthentication):
#     def authenticate_credentials(self, key):
#         try:
#             token = self.model.objects.get(key=key)
#         except self.model.DoesNotExist:
#             raise AuthenticationFailed('Invalid token')
#
#         if not token.user.is_active:
#             raise AuthenticationFailed('User inactive or deleted')
#
#         # This is required for the time comparison
#         utc_now = datetime.utcnow()
#         utc_now = utc_now.replace(tzinfo=timezone.utc)
#
#         if token.created < utc_now - timedelta(hours=24):
#             raise AuthenticationFailed('Token has expired')
#
#         return token.user, token
# class ExpiringTokenAuthentication(TokenAuthentication):
#     def authenticate_credentials(self, key):
#
#         try:
#             token = self.model.objects.get(key=key)
#         except self.model.DoesNotExist:
#             raise AuthenticationFailed('Invalid token')
#
#         if not token.user.is_active:
#             raise AuthenticationFailed('User inactive or deleted')
#
#         utc_now = datetime.utcnow()
#
#         if token.created < utc_now - timedelta(hours=24):
#             raise AuthenticationFailed('Token has expired')
#
#         return token.user, token
