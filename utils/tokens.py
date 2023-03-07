from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        user.timestamp = timestamp
        user.save()
        return f"{user.pk}{timestamp}{user.is_active}"


account_activation_token = TokenGenerator()

password_reset_token = PasswordResetTokenGenerator()
