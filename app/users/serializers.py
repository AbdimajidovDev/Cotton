from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import User


class MeSerializer(serializers.ModelSerializer):
    squad_number = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "full_name", "username", "phone_number", "image", "role", "squad_number")
        extra_kwargs = {
            "id": {"read_only": True},
            "phone_number": {"read_only": True},
        }

    def get_squad_number(self, obj):
        user_squad = obj.squads.first()
        return user_squad.squad_number.number if user_squad and user_squad.squad_number else None

    def validate_full_name(self, value):
        if len(value) <= 3:
            raise ValidationError("Full name must not exceed 3 characters.")
        return value

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get("full_name", instance.full_name)
        instance.username = validated_data.get("username", instance.username)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.image = validated_data.get("image", instance.image)
        instance.role = validated_data.get("role", instance.role)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if not username or not password:
            raise ValidationError("Enter username and password. Please!")

        user = authenticate(username=username, password=password)

        if not user:
            raise ValidationError("Invalid username or password.")

        if not user.is_active:
            raise ValidationError("User is inactive.")

        attrs["user"] = user
        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': 'Invalid or expired token.'
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
