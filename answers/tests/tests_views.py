from rest_framework.test import APITestCase
from accounts.models import User
from answers.models import Answer
from posts.models import Post
from rest_framework.authtoken.models import Token


class AnswersViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first_name = "user"
        cls.last_name = "test"
        cls.users = [
            User.objects.create_user(
                username=f"user{user_id}",
                first_name=cls.first_name,
                last_name=cls.last_name,
                email=f"user{user_id}@mail.com",
                password="1234",
            )
            for user_id in range(0, 2)
        ]
        cls.adm = User.objects.create_superuser(
            username="admUser",
            first_name=cls.first_name,
            last_name=cls.last_name,
            email=f"userAdm@mail.com",
            password="1234",
        )
        cls.post = [
            Post.objects.create(content=f"Teste{answers_id}", user=cls.users[0])
            for answers_id in range(1, 2)
        ]

        cls.answers = [
            Answer.objects.create(
                content=f"Teste{answers_id}", user=cls.users[0], post=cls.post[0]
            )
            for answers_id in range(1, 2)
        ]

    def test_authorization_token_update_answer(self):
        answer = Answer.objects.create(
            content="Eu sei como resolver isso porem nao vou falar",
            user=self.users[1],
            post=self.post[0],
        )

        token = Token.objects.create(user=self.users[0])

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response = self.client.patch(
            f"/api/answers/{answer.id}/", {"content": "uhauehuae"}, format="json"
        )
        self.assertEquals(response.status_code, 403)

        self.assertEquals(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )
