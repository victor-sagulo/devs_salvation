from rest_framework.test import APITestCase
from accounts.models import User
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
            email=f'user{user_id}@mail.com', password='1234') for user_id in range(1, 6)]
        cls.adm = User.objects.create_superuser(username='admUser',
                                                first_name=cls.first_name,
                                                last_name=cls.last_name,
                                                email=f'userAdm@mail.com', password='1234')

    def test_can_list_all_users(self):
        token = Token.objects.create(user=self.users[0])

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get('/api/accounts/')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(self.users)+1, len(response.data))

        for user in self.users:
            self.assertIn(
                AccountsSerializer(instance=user).data,
                response.data
            )

    def test_wrong_keys(self):
        response = self.client.post(
            '/api/accounts/', {'last_name': self.last_name, 'email': 'wrong.com', 'password': '1234'})
        self.assertEquals(response.status_code, 400)
        self.assertEquals(
            response.data['first_name'][0], 'This field is required.')
        self.assertEquals(
            response.data['username'][0], 'This field is required.')
        self.assertEquals(
            response.data['email'][0], 'Enter a valid email address.')

    def test_owner_and_adm_can_update(self):
        main_user = User.objects.create_user(
            username='ownerUser',
            first_name=self.first_name,
            last_name=self.last_name,
            email='seller@mail.com', password='1234')

        other_user = User.objects.create_user(
            username='otherUser',
            first_name=self.first_name,
            last_name=self.last_name,
            email='other@mail.com', password='1234')

        response = self.client.patch(
            f'/api/accounts/{main_user.id}/', {'first_name': 'New Name'})
        self.assertEquals(response.status_code, 401)

        token = Token.objects.create(user=other_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.patch(
            f'/api/accounts/{main_user.id}/', {'first_name': 'New Name'})
        self.assertEquals(response.status_code, 403)

        token = Token.objects.create(user=main_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.patch(
            f'/api/accounts/{main_user.id}/', {'first_name': 'New Name'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['first_name'], 'New Name')

        token = Token.objects.create(user=self.adm)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.patch(
            f'/api/accounts/{main_user.id}/', {'first_name': 'Adm alterou'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['first_name'], 'Adm alterou')
