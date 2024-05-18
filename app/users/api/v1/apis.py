from django.core.validators import MinLengthValidator
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema

from core.services.users import register_user
from . import regex_validators


class RegisterApiView(APIView):

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


