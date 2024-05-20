from datetime import timedelta
from django.core.validators import MinLengthValidator
from django.conf import settings
from rest_framework import status, serializers, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema

from core.services.users import (
    register_user,
    set_new_password,
    check_existing_email,
    reset_password,
    validate_rand_pass,
    set_rand_password
)
from core.services.users import check_old_password
from . import regex_validators


class RegisterApiView(APIView):
    """
    Registering user with email and password.
    """
    class RegisterInputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(validators=(
            MinLengthValidator(limit_value=8),
            regex_validators.number_validator,
            regex_validators.letter_validator,
            regex_validators.special_char_validator
        ))
        password1 = serializers.CharField()

    @extend_schema(request=RegisterInputSerializer)
    def post(self, request: Request, *args, **kwargs) -> Response:
        input_serializer = self.RegisterInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        register_user(
            email=input_serializer.validated_data.get('email', None),
            password=input_serializer.validated_data.get('password', None)
        )
        return Response(status=status.HTTP_201_CREATED)


class ChangePasswordApiView(APIView):
    """
    Changing authenticated user's password.
    """
    permission_classes = [permissions.IsAuthenticated]

    class ChangePasswordInputSerializer(serializers.Serializer):
        old_password = serializers.CharField(required=True)
        new_password = serializers.CharField(validators=(
            MinLengthValidator(limit_value=8),
            regex_validators.number_validator,
            regex_validators.letter_validator,
            regex_validators.special_char_validator
        ), required=True)
        new_password1 = serializers.CharField()

        def validate_old_password(self, old_password):
            request: Request = self.context.get('request')
            return check_old_password(
                input_password=old_password,
                real_password=request.user.password
            )

        def validate(self, attrs):
            if attrs.get('new_password') != attrs.get('new_password1'):
                raise serializers.ValidationError(
                    {'new_password': 'New passwords value dont match.'},
                    code='passwords_not_match'
                )

            return attrs

    @extend_schema(request=ChangePasswordInputSerializer)
    def post(self, request: Request, *args, **kwargs) -> Response:
        input_serializer = self.ChangePasswordInputSerializer(
            data=request.data, context={'request': request}
        )
        input_serializer.is_valid(raise_exception=True)

        try:
            set_new_password(
                user=request.user,
                new_password=input_serializer.validated_data.get('new_password')
            )
            return Response(
                {'message': 'Password changed successfully', 'extra': {}},
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                {'message': f'Something went wrong => {ex}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ResetPasswordApiView(APIView):
    """
    Resetting old password for using in Forgot
    password option in the Front-End.
    """

    class ResetPasswordInputSerializer(serializers.Serializer):
        email = serializers.EmailField()

        def validate_email(self, email):
            if not check_existing_email(email=email):
                raise serializers.ValidationError(
                    'There is no active user with the provided email.',
                    code='no_active_email'
                )
            return email
    
    @extend_schema(request=ResetPasswordInputSerializer)
    def post(self, request: Request, *args, **kwargs) -> Response:
        input_serializer = self.ResetPasswordInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            reset_password(
                email=input_serializer.validated_data.get('email')
            )
            rand_pass_timeout: timedelta = settings.RESET_PASSWORD_TIMEOUT
            return Response(
                {
                    'message': f'The new password was sent for you. limit time is {
                        rand_pass_timeout.total_seconds()
                    } seconds',
                    'extra': {}
                },
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                {'message': f'Something went wrong => {ex}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VerifyRandPasswordApiView(APIView):
    """
    Retrieve an input named password, this is the
    random password which we stored in redis cache and
    also sent it via email to client, if it was true
    password changed to that random string temporary.
    """

    class VerifyRandPasswordInputSerializer(serializers.Serializer):
        rand_password = serializers.CharField()

    @extend_schema(request=VerifyRandPasswordInputSerializer)
    def post(self, request: Request, *args, **kwargs) -> Response:
        input_serializer = self.VerifyRandPasswordInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        # Return APIException or tuple[bool, str(cached_email)]
        _, cached_email = validate_rand_pass(
            rand_pass=input_serializer.validated_data.get('rand_password')
        )
        set_rand_password(
            email=cached_email,
            rand_password=input_serializer.validated_data.get('rand_password')
        )
        return Response(
            {'message': 'Password changed successfully', 'extra': {}},
            status=status.HTTP_200_OK
        )
