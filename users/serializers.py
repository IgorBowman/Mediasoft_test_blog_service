from rest_framework import serializers

from .models import CustomUser


class CreateCustomUserSerializer(serializers.ModelSerializer):
    """ Serializer for create new user. """

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', ]

    def create(self, validated_data):
        # Использовать метод create_user, который мы
        # написали ранее, для создания нового пользователя.
        return CustomUser.objects.create_user(**validated_data)
