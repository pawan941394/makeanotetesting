from datetime import time
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import UserProfile

import six

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        verifyEmail = UserProfile.objects.get(user=user)
        is_verify = verifyEmail.is_email_verified
        return six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(is_verify)


generate_token = TokenGenerator()