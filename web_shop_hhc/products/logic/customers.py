from ..models import SecretString, User
from datetime import datetime, timezone


class PasswordReset:
    def _secret_validation(self, secret_string):
        secret_data = SecretString.objects.get(secret_string=secret_string)
        if not secret_data:
            return False
        secret_creation_time = secret_data.creation_time
        current_time = datetime.now(timezone.utc).astimezone()
        delta_time = (current_time - secret_creation_time).seconds / 60
        if delta_time >= 15:
            return False
        self.user_reset_password = secret_data.user
        return True

    def __init__(self, secret_string):
        self.secret_string = secret_string
        self.secret_is_valid = self._secret_validation(secret_string)
