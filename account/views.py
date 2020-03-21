from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from .serializers import UserSerializer
from Blog.settings import EMAILHUNTER_TOKEN, EMAILHUNTER_URL
import requests as r


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # password validation
        if len(request.POST["password"]) < 8:
            return Response({'text': 'too short password'}, status=status.HTTP_400_BAD_REQUEST, )

        # email (in addition to EmailField) validation
        email = request.POST["email"]
        email_data = r.get(
            EMAILHUNTER_URL,
            params={'email': email, 'api_key': EMAILHUNTER_TOKEN},
            headers={'Content-type': 'application/json'}
        ).json()['data']
        email_block = email_data['block']
        if email_block:
            return Response({'text': 'email validation failed'}, status=status.HTTP_400_BAD_REQUEST, )
        email_accept_all = email_data['accept_all']

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        response = serializer.data
        response['email_check'] = "passed"
        response['email_block'] = email_block
        response['email_accept_all'] = email_accept_all

        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    def get_permissions(self):
        # allow unauthenticated users to list, retrieve and create new users
        permission = (AllowAny() if self.action in ('create', )
                      else IsAdminUser())
        return [permission]

