from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api_yamdb.settings import DEFAULT_FROM_EMAIL

User = get_user_model()


class RegistrationUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',)

    def create(self, validated_data):
        email = validated_data['email']
        user = get_object_or_404(User, email=email)
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
            'Ваш код подтверждения',
            confirmation_code,
            DEFAULT_FROM_EMAIL,
            [email],
        )
        return email


class AuthenticationTokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('email', 'confirmation_code')

    def validate(self, data):
        email = data['email']
        send_confirmation_code = data['confirmation_code']
        user = get_object_or_404(User, email=email)
        if send_confirmation_code == user.confirmation_code:
            refresh = TokenObtainPairSerializer.get_token(user)
            data['token'] = str(refresh.access_token)
            return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'username',
            'bio',
            'role'
        )
