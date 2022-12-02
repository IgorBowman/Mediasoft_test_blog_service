from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Blogs, Posts, Comments, Tags


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username']


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = '__all__'


class AddAuthorToBlogSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        authors = validated_data.pop('authors')
        current_user = self.context['request'].user

        for author in authors:
            if (author != current_user) \
                    and (author not in instance.authors.all()):
                instance.authors.add(author)
        return instance

    class Meta:
        model: Blogs
        fields = ['authors']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class CreateSubscriptionSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        current_user = self.context['request'].user

        if current_user not in instance.subscription.all():
            instance.subscription.add(current_user)
        return instance

    class Meta:
        model = Blogs
        fields = ['subscription']
