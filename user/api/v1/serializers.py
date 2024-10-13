from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):

    avatar = serializers.URLField(read_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False, write_only=True)

    def create(self, validated_data: dict[str, str]) -> User:
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'avatar')


class UserPublicSerializer(serializers.ModelSerializer):

    avatar = serializers.URLField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar', 'first_name', 'last_name')
