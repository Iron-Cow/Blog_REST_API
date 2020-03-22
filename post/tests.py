from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Post
from account.tests import get_access_header

class PostTests(TestCase):
    def setUp(self):
        usr_admin = User.objects.create_superuser(username='admin1', email='admin@email.com', password='admin_pass')
        usr_admin.raw_password = 'admin_pass'
        usr1 = User.objects.create_user(username='test1', email='test1@email.com', password='test1_pass')
        usr1.raw_password = 'test1_pass'
        usr2 = User.objects.create_user(username='test2', email='test2@email.com', password='test2_pass')
        usr2.raw_password = 'test2_pass'

        post1 = Post.objects.create(title='Title1', content='Test1', user=usr_admin)
        post2 = Post.objects.create(title='Title2', content='Test2', user=usr1)
        post3 = Post.objects.create(title='Title3', content='Test3', user=usr2)

        self.users = [usr_admin, usr1, usr2]
        self.posts = [post1, post2, post3]

    def test_unauthenticated_user_request_post_list(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(len(response.json()), len(self.posts))

        db_id = {post.id for post in self.posts}
        response_id = {post['id'] for post in response.json()}
        self.assertEqual(db_id, response_id)

    def test_unauthenticated_user_request_post_details(self):
        post = self.posts[0]
        path = reverse('post-detail', kwargs={'pk': post.id})
        response = self.client.get(path).json()

        self.assertEqual(response['id'], post.id)
        self.assertEqual(response['title'], post.title)
        self.assertEqual(response['content'], post.content)
        self.assertEqual(response['user'], post.user.id)

    def test_authenticated_user_post_create(self):
        user = self.users[1]
        auth_header = get_access_header(self.client, user)
        post_data = {'title': 'test', 'content': 'test'}
        response = self.client.post(reverse('post-list'), data=post_data,
                                    **auth_header)
        self.assertEqual(response.status_code, 201)

        post_id = int(response.json()['id'])
        post_to_check = Post.objects.get(id=post_id)
        self.assertEqual(post_to_check.user.id, user.id)

    def test_unauthenticated_user_post_create(self):
        post_data = {'title': 'test', 'content': 'test'}
        response = self.client.post(reverse('post-list'), data=post_data)
        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_post_update(self):
        user = self.users[1]
        auth_header = get_access_header(self.client, user)
        user_post = Post.objects.get(user=user)
        post_data = {'title': 'Updated', 'content': 'Updated text by owner'}
        response = self.client.patch(reverse('post-detail', kwargs={'pk': user_post.id}),
                                     content_type='application/json', data=post_data,
                                     **auth_header)
        self.assertEqual(response.status_code, 200)

        post_id = int(response.json()['id'])
        post_to_check = Post.objects.get(id=post_id)
        self.assertEqual(post_to_check.user.id, user.id)

    def test_unauthenticated_user_post_update_fail(self):
        user = self.users[1]
        user_post = Post.objects.get(user=user)
        post_data = {'title': 'Updated', 'content': 'Updated text by owner'}
        response = self.client.patch(reverse('post-detail', kwargs={'pk': user_post.id}),
                                     content_type='application/json', data=post_data)
        self.assertEqual(response.status_code, 401)

    def test_notauthor_user_post_update_fail(self):
        user = self.users[1]
        user_stranger = self.users[2]
        auth_header = get_access_header(self.client, user_stranger)
        user_post = Post.objects.get(user=user)
        post_data = {'title': 'Updated', 'content': 'Updated text by owner'}
        response = self.client.patch(reverse('post-detail', kwargs={'pk': user_post.id}),
                                     content_type='application/json', data=post_data,
                                     **auth_header)
        self.assertEqual(response.status_code, 401)

    def test_notauthor_admin_post_update(self):
        user = self.users[1]
        user_stranger_admin = self.users[0]
        auth_header = get_access_header(self.client, user_stranger_admin)
        user_post = Post.objects.get(user=user)
        post_data = {'title': 'Updated', 'content': 'Updated text by owner'}
        response = self.client.patch(reverse('post-detail', kwargs={'pk': user_post.id}),
                                     content_type='application/json', data=post_data,
                                     **auth_header)
        self.assertEqual(response.status_code, 200)

        #check if post-creator-id not changed
        post_id = int(response.json()['id'])
        post_to_check = Post.objects.get(id=post_id)
        self.assertEqual(post_to_check.user.id, user.id)


    def test_unauthenticated_user_post_like_fail(self):
        user = self.users[0]
        user_post = Post.objects.get(user=user)
        response = self.client.post(reverse('post-like', kwargs={'pk': user_post.id}),)
        self.assertEqual(response.status_code, 401)


    def test_authenticated_user_post_like(self):
        user = self.users[0]
        auth_header = get_access_header(self.client, user)
        user_post = Post.objects.get(user=user)
        self.assertFalse(user in user_post.liked_users.all())
        self.client.post(reverse('post-like', kwargs={'pk': user_post.id}), **auth_header)
        self.assertTrue(user in user_post.liked_users.all())


    def test_unauthenticated_user_post_like_remove_fail(self):
        user = self.users[0]
        user_post = Post.objects.get(user=user)
        response = self.client.post(reverse('post-remove_like', kwargs={'pk': user_post.id}), )
        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_post_like_remove(self):
        user = self.users[0]
        auth_header = get_access_header(self.client, user)
        user_post = Post.objects.get(user=user)
        self.assertFalse(user in user_post.liked_users.all())
        self.client.post(reverse('post-like', kwargs={'pk': user_post.id}), **auth_header)
        self.assertTrue(user in user_post.liked_users.all())
        self.client.post(reverse('post-remove_like', kwargs={'pk': user_post.id}), **auth_header)
        self.assertFalse(user in user_post.liked_users.all())

    def test_authenticated_user_post_like_remove_twice_fail(self):
        user = self.users[0]
        auth_header = get_access_header(self.client, user)
        user_post = Post.objects.get(user=user)
        self.assertFalse(user in user_post.liked_users.all())
        self.client.post(reverse('post-like', kwargs={'pk': user_post.id}), **auth_header)
        self.assertTrue(user in user_post.liked_users.all())
        self.client.post(reverse('post-remove_like', kwargs={'pk': user_post.id}), **auth_header)
        response = self.client.post(reverse('post-remove_like', kwargs={'pk': user_post.id}), **auth_header)
        self.assertEqual("please like this post first before like removing", response.json()["status"])

    def test_authenticated_user_post_like_twice_fail(self):
        user = self.users[0]
        auth_header = get_access_header(self.client, user)
        user_post = Post.objects.get(user=user)
        self.assertFalse(user in user_post.liked_users.all())
        self.client.post(reverse('post-like', kwargs={'pk': user_post.id}), **auth_header)
        self.assertTrue(user in user_post.liked_users.all())
        response = self.client.post(reverse('post-like', kwargs={'pk': user_post.id}), **auth_header)
        self.assertEqual("you already liked this post", response.json()["status"])

