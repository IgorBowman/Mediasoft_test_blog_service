from rest_framework import serializers

from .models import CustomUser


class CreateCustomUserSerializer(serializers.ModelSerializer):
    """ Serializer for create new user. """

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
