from django.utils.translation import gettext_lazy as _

from users.models import BaseUser


def register_user(*, email: str, password: str) -> BaseUser:
    """
    Registering users with the provided info.
    """
    user = BaseUser(email=email, password=password)
    user.full_clean()
    user.save()