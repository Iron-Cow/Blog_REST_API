from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Post
from .serializers import PostSerializer


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_permissions(self):
        # allow unauthenticated users to list, retrieve and create new users
        permission = (AllowAny() if self.action in ('list', 'retrieve')
                      else IsAuthenticated())
        return [permission]

    def update(self, request, pk=None, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        # allow change/delete the post only by it's author
        if post.user == request.user or request.user.is_superuser:
            return super().update(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['post'], url_name='like', permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        if post.liked_users.filter(pk=user.pk).exists():
            return Response({'status': 'you already liked this post'})
        else:
            post.liked_users.add(request.user)
            return Response({'status': 'your like added'})

    @action(detail=True, methods=['post'], url_name='remove_like', permission_classes=[IsAuthenticated])
    def remove_like(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        if not post.liked_users.filter(pk=user.pk).exists():
            return Response({'status': 'please like this post first before like removing'})
        else:
            post.liked_users.remove(request.user)
            return Response({'status': 'your like removed'})

