from django.contrib.auth.models import User
from .models import Post

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'content', 'user', 'liked_users', 'timestamp', )
        read_only_fields = ('liked_users', 'timestamp', 'user')

    def create(self, validated_data):
        """Auto post sign creation (for authenticated users only)"""
        return Post.objects.create(user=self.context['request'].user, **validated_data)
