"""
serializers.py: File, containing serializers for a jauth application.
"""


from typing import ClassVar, Optional
from rest_framework import serializers
from jauth.models import User
from jauth.tokens import Token


class UserSerializer(serializers.ModelSerializer):
    """
    UserSerializer: Serializes User object to py-native types and vice versa.

    Args:
        serializers.ModelSerializer (_type_): Builtin superclass for a UserSerliazer.
    """

    class Meta:
        model: ClassVar[type[User]] = User
        fields: ClassVar[tuple] = (
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'date_joined',
            'last_login',
            'is_active',
            'is_staff',
        )
        read_only_fields: ClassVar[tuple] = (
            'date_joined',
            'last_login',
            'is_active',
            'is_staff',
        )


class AccessTokenSerializer(serializers.Serializer):
    """
    AccessTokenSerializer: Serializes token form to py-native types and vice versa.

    Args:
        serializers.Serializer (_type_): Builtin superclass for an AccessTokenSerializer.

    Raises:
        serializers.ValidationError: Raises when email adress is not specified.
        serializers.ValidationError: Raises when password is not specified.
        serializers.ValidationError: Raises when spicified email adress is not found.
        serializers.ValidationError: Raises when spicified password is not correct.
        serializers.ValidationError: Raises when account is deactivated.
    """

    token_class: ClassVar[type[Token]] = Token

    email = serializers.CharField(
        max_length=320,
        min_length=3,
        write_only=True,
    )

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    def validate(self, data: dict) -> dict:
        """
        validate: Validates request data.

        Args:
            data (dict): Incoming data.

        Raises:
            serializers.ValidationError: Raises when email adress is not specified.
            serializers.ValidationError: Raises when password is not specified.
            serializers.ValidationError: Raises when spicified email adress is not found.
            serializers.ValidationError: Raises when spicified password is not correct.
            serializers.ValidationError: Raises when account is deactivated.

        Returns:
            dict: Dict with new access token and refresh token.
        """

        email: Optional[str] = data.get('email', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required.',
            )

        password: Optional[str] = data.get('password', None)

        if password is None:
            raise serializers.ValidationError(
                'A password is required.',
            )

        user: Optional[User] = User.objects.filter(email=email).first()

        if user is None:
            raise serializers.ValidationError(
                'A user with this email is not found.',
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                'Password is not correct.',
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'Account is deactivated.',
            )

        access_token, refresh_token = self.token_class.for_user(user)

        return {
            'access': access_token.token,
            'refresh': refresh_token.token,
        }


class RefreshTokenSerializer(serializers.Serializer):
    """
    RefreshTokenSerializer: Serializes refresh-token form to py-native types and vice versa.

    Args:
        serializers.Serializer (_type_): Builtin superclass for an RefreshTokenSerializer.

    Raises:
        serializers.ValidationError: Raises when refresh token is not specified.
        serializers.ValidationError: Raises when refresh token is expired.
        serializers.ValidationError: Raises when refresh token is invalid.
        serializers.ValidationError: Raises when refresh token is not correct.
    """

    token_class: ClassVar[type[Token]] = Token

    refresh = serializers.CharField(
        max_length=128,
        min_length=32,
        write_only=True,
    )

    def validate(self, data: dict) -> dict:
        """
        validate: Validates request data.

        Args:
            data (dict): Incoming data.

        Raises:
            serializers.ValidationError: Raises when refresh token is not specified.
            serializers.ValidationError: Raises when refresh token is expired.
            serializers.ValidationError: Raises when refresh token is invalid.
            serializers.ValidationError: Raises when refresh token is not correct.

        Returns:
            dict: Dict with new access token and refresh token.
        """

        user_refresh_token: Optional[str] = data.get('refresh', None)

        if user_refresh_token is None:
            raise serializers.ValidationError(
                'Refresh token is required.',
            )

        token: Token = self.token_class(token=user_refresh_token, type='refresh')

        is_verified = token.verify()

        if not is_verified:
            if token.expired:
                raise serializers.ValidationError(
                    'Token is expired.',
                )

            if token.invalid:
                raise serializers.ValidationError(
                    'Token is invalid.',
                )

        user: Optional[User] = token.get_user_by_token()

        if user is None:
            raise serializers.ValidationError(
                'Token is not correct.',
            )

        access_token, refresh_token = self.token_class.for_user(user)

        return {
            'access': access_token.token,
            'refresh': refresh_token.token,
        }
