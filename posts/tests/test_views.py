from rest_framework.test import APITestCase
from accounts.models import User
from posts.models import Post
from posts.serializers import PostSerializer
from accounts.serializers import AccountsSerializer
from rest_framework.authtoken.models import Token


class UsersViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first_name = 'user'
        cls.last_name = 'test'
        cls.users = [User.objects.create_user(
            username=f'user{user_id}',
            first_name=cls.first_name,
            last_name=cls.last_name,
            email=f'user{user_id}@mail.com', password='1234') for user_id in range(0, 2)]
        cls.adm = User.objects.create_superuser(username='admUser',
                                                first_name=cls.first_name,
                                                last_name=cls.last_name,
                                                email=f'userAdm@mail.com', password='1234')
        cls.posts = [Post.objects.create(
            content=f'Teste{post_id}', user=cls.users[0]) for post_id in range(1, 2)]

    def can_list_all_posts(self):

        response = self.client.get('/api/posts/')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(self.users), len(response.data))

        for post in self.posts:
            self.assertIn(
                PostSerializer(instance=post).data,
                response.data
            )

    def test_wrong_keys(self):

        token = Token.objects.create(user=self.users[0])

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(
            '/api/posts/', {'content': 'Estou tendo problemas com o meu codigo'})
        self.assertEquals(response.status_code, 400)
        self.assertEquals(
            response.data['tags'][0], 'This field is required.')

    def test_owner_and_adm_can_update_and_delete(self):

        post = Post.objects.create(content=f'Teste', user=self.users[0])

        token = Token.objects.create(user=self.users[1])

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.patch(
            f'/api/posts/{post.id}/', {'content': 'New question'})
        self.assertEquals(response.status_code, 403)

        token = Token.objects.create(user=self.users[0])

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.patch(
            f'/api/posts/{post.id}/', {'content': 'New question'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['content'], 'New question')

        token = Token.objects.create(user=self.adm)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.patch(
            f'/api/posts/{post.id}/', {'content': 'Adm edited'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['content'], 'Adm edited')

        token = Token.objects.get(user=self.users[0])

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.delete(f'/api/posts/{post.id}/')
        self.assertEquals(response.status_code, 204)
