from django.test import TestCase
from accounts.models import User
from django.db import IntegrityError


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "gabriel.castedo1@gmail.com"
        cls.username = "MrBoliva"
        cls.first_name = "Gabriel"
        cls.last_name = "Castedo"
        cls.password = "1234"

        cls.user = User.objects.create_user(
            email=cls.email,
            username=cls.username,
            first_name=cls.first_name,
            last_name=cls.last_name,
            password=cls.password,
        )

    def test_email_unique(self):
        with self.assertRaises(IntegrityError):
            email_2 = User.objects.create_user(
                email="gabriel.castedo1@email.com",
                username="MrBoliva",
                first_name="gabriel",
                last_name="castedo",
                password="123",
            )

            email_2.save()

    def test_first_nam(self):
        user_1 = User.objects.get(id=1)
        max_length = user_1._meta.get_field("first_name").max_length
        self.assertEquals(max_length, 125)

    def test_user_has_information_fields(self):
        self.assertEquals(self.user.email, self.email)
        self.assertEquals(self.user.username, self.username)
        self.assertEqual(self.user.first_name, self.first_name)
        self.assertEqual(self.user.last_name, self.last_name)
        self.assertEquals(self.user.check_password(self.password), True)
