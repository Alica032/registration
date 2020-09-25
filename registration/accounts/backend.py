from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from .models import User
from django.db.models import Q


class SettingsBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None and email is None or password is None:
            return
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760)
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
