from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
from datetime import timedelta
import hashlib
import base64


class CustomTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        # hash value with timestamp to include expiration logic
        return f"{user.pk}{user.password}{timestamp}"

    def check_token(self, user, token):
        # split token to user data and timestamp
        try:
            token_data, timestamp = token.rsplit(":", 1)
            timestamp = base64.urlsafe_b64decode(timestamp.encode()).decode()
            timestamp = timezone.make_aware(timezone.datetime.fromtimestamp(int(timestamp)))
        except Exception:
            return False

        # check if token has expired
        if timezone.now() > timestamp + timedelta(minutes=10):
            return False

        # check if token matches the hash
        return super().check_token(user, token_data)

    def make_token(self, user):
        # get current time and create a token
        timestamp = str(int(timezone.now().timestamp()))
        token = super().make_token(user)
        return f"{token}:{timestamp}"
