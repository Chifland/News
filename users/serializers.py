from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User

class UserValidateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class AuthorizationValidateSerializer(UserValidateSerializer):
    pass

class RegistrationVlidateSerializer(UserValidateSerializer):

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
            raise ValidationError('User already exist')
        except User.DoesNotExist:
            return username


