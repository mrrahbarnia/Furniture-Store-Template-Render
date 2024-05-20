import uuid

from datetime import timedelta
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password
from django.core.cache import cache
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import APIException

from users.models import BaseUser

# ================= Dependencies ================= #
def random_password() -> str:
    """Return new random password for reset password endpoint."""
    return str(uuid.uuid4())[:9]


# ================= Authentication services ================= #
def register_user(*, email: str, password: str) -> BaseUser:
    """
    Registering users with the provided info.
    """
    user = BaseUser(email=email, password=password)
    user.full_clean()
    user.save()

def check_old_password(*, input_password: str, real_password) -> str | serializers.ValidationError:
    """
    Check entered old password validity.
    """
    if check_password(input_password, real_password):
        return input_password
    else:
        raise serializers.ValidationError(
            'Old password is wrong.',
            code='wrong_old_password'
        )

def set_new_password(*, user: BaseUser, new_password: str) -> None:
    """
    Set a new given password for provided user and return nothing.
    """
    user.set_password(new_password)
    user.save(update_fields=['password'])

def check_existing_email(*, email: str) -> bool:
    """
    Check the provided email for existing and
    return True if it exists and return False if not.
    """
    return BaseUser.objects.filter(email=email).exists()

def reset_password(*, email: str) -> None:
    """
    Set a random password into redis memory with limited timeout.
    """
    rand_password: str = random_password()
    rand_pass_timeout: timedelta = settings.RESET_PASSWORD_TIMEOUT
    cache.set(
        key=f'random-pass:{rand_password}',
        value=f'{email}',
        timeout=rand_pass_timeout.total_seconds()
    )

    # TODO For PRODUCTION:
    # Send a link to provided email via celery for entering random pass by client.

def validate_rand_pass(*, rand_pass: str) -> tuple[bool, str] | APIException:
    """
    Validating entered random password from user
    to check wether if it is in redis memory or not.
    """
    if cached_email:= cache.get(key=f'random-pass:{rand_pass}'):
        return True, cached_email
    raise APIException(
        'The provided password is wrong or the time limit has been expired.'
    )

def set_rand_password(*, email: str, rand_password: str) -> None:
    """
    Set the given random password for user with specific cached email.
    """
    user = BaseUser.objects.get(email=email)
    user.set_password(rand_password)
    user.save(update_fields=['password'])
