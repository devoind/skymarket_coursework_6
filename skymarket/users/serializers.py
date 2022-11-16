from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers

from users.models import User


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    pass


class CurrentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'image']
