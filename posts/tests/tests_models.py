from django.test import TestCase

from accounts.models import User
from posts.models import Post
from tags.models import Tag


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_example = {
            "email": "guimeuchampinho@filhonhodopapai.com",
            "username": "Champinho",
            "first_name": "Guilherme",
            "last_name": "Silva Sagulo",
            "password": "12345"
        }

        cls.user = User.objects.create(**user_example)

        cls.content = "Estou tendo problemas com o meu codigo"

        post = Post.objects.create(
            content=cls.content, user=cls.user)

        cls.post = post

    def test_owner_post(self):
        post = Post.objects.get(id=1)

        self.assertEquals(post.user, self.user)

    def test_tags_creation_of_post(self):
        post = Post.objects.get(id=1)

        tags = [{"name": "Python"}, {"name": "DjangoORM"}]

        post.tags.set([Tag.objects.create(**tag) for tag in tags])

        self.assertEquals(post.tags.count(), len(tags))

    def test_post_content(self):
        self.assertEqual(self.post.content, self.content)
        self.assertTrue(self.post.created_at)
        self.assertTrue(self.post.updated_at)
        self.assertEquals(self.post.usefull_post.count(), 0)
