from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'display_name']

    def validate_email(self, value):
        """
        Ensure the email is unique.
        """
        if CustomUser.objects.filter(email=value).exists():
            raise ValidationError("Email is already taken.")
        return value

    def validate_password(self, value):
        """
        Ensure the password is sufficiently strong (optional).
        You can customize this as needed.
        """
        if len(value) < 6:
            raise ValidationError("Password must be at least 6 characters long.")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = CustomUser.objects.create(**validated_data)
        return user