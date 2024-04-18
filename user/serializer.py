from typing import Any, Dict
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth import authenticate


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        res = super().validate(attrs)
        res['email'] = self.user.email
        return res

class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("id", "email", "password", "password1")
        extra_kwargs = {'password' : {'write_only' : True}, 'required':True}

    def validate(self, attrs):
        password1 = attrs.pop('password1')
        if attrs['password'] != password1:
            raise serializers.ValidationError("Passwords do not match !")
        return attrs
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    

class UserLoginSerializer(serializers.ModelSerializer):
    access_token = serializers.CharField(max_length=200, read_only=True)
    refresh_token = serializers.CharField(max_length=200, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'access_token', 'refresh_token']





                   