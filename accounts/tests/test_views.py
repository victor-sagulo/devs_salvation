from rest_framework.test import APITestCase
from accounts.models import User
from accounts.serializers import UserSerializer
from rest_framework.authtoken.models import Token


class UsersViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first_name = 'user'
        cls.last_name = 'test'
        cls.users = [User.objects.create_user(
            first_name=cls.first_name,
            last_name=cls.last_name,
            email=f'user{user_id}@mail.com', password='1234') for user_id in range(1, 6)]

    def test_can_list_all_users(self):
        response = self.client.get('/api/accounts/')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(self.users), len(response.data))

        for user in self.users:
            self.assertIn(
                UserSerializer(instance=user).data,
                response.data
            )

    def test_create_normal_user(self):
        response = self.client.post('/api/accounts/', {'first_name': self.first_name,
                                    'last_name': self.last_name, 'email': 'normaluser@mail.com', 'password': '1234'})
        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data['is_seller'], False)

    def test_create_seller(self):
        response = self.client.post('/api/accounts/', {'first_name': self.first_name,
                                    'last_name': self.last_name, 'email': 'selleruser@mail.com', 'password': '1234', 'is_seller': True})
        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data['is_seller'], True)

    def test_wrong_keys(self):
        response = self.client.post(
            '/api/accounts/', {'last_name': self.last_name, 'email': 'wrong.com', 'password': '1234'})
        self.assertEquals(response.status_code, 400)
        self.assertEquals(
            response.data['first_name'][0], 'This field is required.')
        self.assertEquals(
            response.data['email'][0], 'Enter a valid email address.')

    def test_seller_login(self):
        User.objects.create_user(
            first_name=self.first_name,
            last_name=self.last_name,
            email='seller@mail.com', is_seller=True, password='1234')
        response = self.client.post(
            '/api/login/', {'email': 'seller@mail.com', 'password': '1234'})
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.data['token'])

    def test_normal_login(self):
        User.objects.create_user(
            first_name=self.first_name,
            last_name=self.last_name,
            email='normal@mail.com', password='1234')
        response = self.client.post(
            '/api/login/', {'email': 'normal@mail.com', 'password': '1234'})
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.data['token'])

    def test_only_owner_can_update(self):
        main_user = User.objects.create_user(
            first_name=self.first_name,
            last_name=self.last_name,
            email='seller@mail.com', is_seller=True, password='1234')

        other_user = User.objects.create_user(
            first_name=self.first_name,
            last_name=self.last_name,
            email='other@mail.com', is_seller=True, password='1234')

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

    def test_only_adm_can_deactivate(self):
        main_user = User.objects.create_user(
            first_name=self.first_name,
            last_name=self.last_name,
            email='seller@mail.com', is_seller=True, password='1234')
        adm = User.objects.create_superuser(first_name=self.first_name,
                                            last_name=self.last_name,
                                            email='adm@mail.com', password='1234')
        normal_token = Token.objects.create(user=main_user)
        adm_token = Token.objects.create(user=adm)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + normal_token.key)

        response = self.client.patch(
            f'/api/accounts/{main_user.id}/management/', {'is_active': False})

        self.assertEquals(response.status_code, 403)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + adm_token.key)

        response = self.client.patch(
            f'/api/accounts/{main_user.id}/management/', {'is_active': False})

        self.assertEquals(response.status_code, 200)
        self.assertFalse(response.data['is_active'])

    def test_only_adm_can_reactivate(self):
        main_user = User.objects.create_user(
            first_name=self.first_name,
            last_name=self.last_name,
            email='seller@mail.com', is_seller=True, password='1234')
        adm = User.objects.create_superuser(first_name=self.first_name,
                                            last_name=self.last_name,
                                            email='adm@mail.com', password='1234')

        adm_token = Token.objects.create(user=adm)
        normal_token = Token.objects.create(user=main_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + adm_token.key)

        response = self.client.patch(
            f'/api/accounts/{main_user.id}/management/', {'is_active': False})
        self.assertEquals(response.status_code, 200)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + normal_token.key)

        response = self.client.patch(
            f'/api/accounts/{main_user.id}/management/', {'is_active': True})
        self.assertEquals(response.status_code, 401)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + adm_token.key)

        response = self.client.patch(
            f'/api/accounts/{main_user.id}/management/', {'is_active': True})
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.data['is_active'])
