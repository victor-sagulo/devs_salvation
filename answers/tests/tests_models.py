from django.test import TestCase

from accounts.models import User
from answers.models import Answer
from posts.models import Post


class AnswerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_example = {
            "email": "guimeuchampinho@filhonhodopapai.com",
            "username": "Champinho",
            "first_name": "Guilherme",
            "last_name": "Silva Sagulo",
            "password": "12345"
        }

        user_to_like_example = {
            "email": "marcos@filhonhodopapai.com",
            "username": "Marquinhos",
            "first_name": "Marcos",
            "last_name": "Mafei",
            "password": "12345"
        }

        user_to_dislike_example = {
            "email": "casteado@filhonhodopapai.com",
            "username": "Castedinho",
            "first_name": "Gabriel",
            "last_name": "Casteado",
            "password": "12345"
        }

        post_example = {
            "content": "Meu código não funciona"
        }

        cls.user = User.objects.create(**user_example)
        cls.user_like = User.objects.create(**user_to_like_example)
        cls.user_dislike = User.objects.create(**user_to_dislike_example)

        cls.post = Post.objects.create(**post_example, user=cls.user)

        cls.content = "É só fazer direito que você resolve o seu problema"

        cls.answer = Answer.objects.create(
            content=cls.content, user=cls.user, post=cls.post)

    def test_like(self):
        answer = Answer.objects.get(id=1)

        self.assertEquals(answer.likes.count(), 0)

        answer.likes.add(self.user_like)

        self.assertEquals(answer.likes.count(), 1)

    def test_dislike(self):
        answer = Answer.objects.get(id=1)

        self.assertEquals(answer.dislikes.count(), 0)

        answer.dislikes.add(self.user_dislike)

        self.assertEquals(answer.dislikes.count(), 1)

    def test_post_content(self):
        self.assertEqual(self.answer.content, self.content)
        self.assertTrue(self.answer.created_at)
        self.assertTrue(self.answer.updated_at)

    def test_owner_and_post_of_answer(self):
        self.assertEquals(self.answer.post, self.post)
        self.assertEquals(self.answer.user, self.user)
