from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth.models import User
from .models import CustomUser as User


class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        user_exist = User.objects.filter(email=username).exists()
        if user_exist:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        else:
            return None
        return None

