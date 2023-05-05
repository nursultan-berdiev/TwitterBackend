from rest_framework import serializers
from django.contrib.auth import password_validation as pv

from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'profile_avatar']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('Пароль не совпадают')
        for sigh in attrs['password']:
            if not sigh.isalnum():
                raise serializers.ValidationError('Пароль не должен содержать спец. символы')
        if len(attrs['password']) < 8:
            raise serializers.ValidationError('Пароль должен содержать минимум 8 символов')
        if not any(ch.isdigit() for ch in attrs['password']):
            raise serializers.ValidationError('Пароль должен содержать минимум 1 цифру')
        if not any(ch.isalpha() for ch in attrs['password']):
            raise serializers.ValidationError('Пароль должен содержать минимум 1 букву')
        return attrs

    def validate_password(self, value):
        try:
            pv.validate_password(value)
        except pv.ValidationError as e:
            raise serializers.ValidationError(e)
        else:
            return value

    def create(self, validated_data):
        user = User(
            username=validated_data.get('username'),
            profile_avatar=validated_data.get('profile_avatar')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "date_joined", "email"]
