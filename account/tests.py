from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


def get_access_header(client, user):
    """Get access header login-required operations."""

    response = client.post(
        reverse('token-obtain'),
        data={'username': user.username, 'password': user.raw_password},
        headers={'Content-type': 'application/json'}
    )
    token = response.json()['access']
    return {'HTTP_AUTHORIZATION': f'Bearer {token}'}


class UserTests(TestCase):
    def setUp(self):
        usr_admin = User.objects.create_superuser(
            username='admin1', email='admin@email.com', password='admin_pass')
        usr_admin.raw_password = 'admin_pass'
        usr1 = User.objects.create_user(
            username='test1', email='test1@email.com', password='test1_pass')
        usr1.raw_password = 'test1_pass'
        usr2 = User.objects.create_user(
            username='test2', email='test2@email.com', password='test2_pass')
        usr2.raw_password = 'test2_pass'

        self.users = [usr_admin, usr1, usr2]

    def test_regular_user_request_user_list(self):
        response = self.client.get(reverse('user-list'))
        self.assertNotEqual(len(response.json()), len(self.users))

    def test_admin_user_request_user_list(self):
        user = self.users[0]
        auth_header = get_access_header(self.client, user)
        response = self.client.get(reverse('user-list'),
                                   **auth_header)
        self.assertEqual(len(response.json()), len(self.users))

    def test_user_sign_up(self):
        post_data = {'username': 'RegularUser1',
                     'email': 'Regular@email.com',
                     'password': 'Regular_pass'}
        response = self.client.post(reverse('user-list'), data=post_data,
                                    )
        self.assertEqual(response.status_code, 201)
