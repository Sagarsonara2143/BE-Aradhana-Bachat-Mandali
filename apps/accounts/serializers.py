from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "mobile_number", "full_name", "role", "is_active"]
        read_only_fields = fields


class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(help_text="Email or mobile number")
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, attrs):
        identifier = attrs["identifier"].strip()
        password = attrs["password"]

        user = User.objects.filter(email__iexact=identifier).first()
        if user is None:
            user = User.objects.filter(mobile_number=identifier).first()

        if user is None or not user.check_password(password) or not user.is_active:
            raise serializers.ValidationError("Invalid credentials or inactive account.")

        # Re-authenticate through the backend to run any extra checks.
        auth_user = authenticate(
            self.context.get("request"), username=user.email, password=password
        )
        if auth_user is None:
            raise serializers.ValidationError("Invalid credentials or inactive account.")

        attrs["user"] = auth_user
        return attrs

    def to_tokens(self) -> dict:
        user = self.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        refresh["role"] = user.role
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data,
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
