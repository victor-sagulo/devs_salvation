from django.db import models


class Answer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    likes = models.ManyToManyField(
        "accounts.User", related_name="liked_posts")
    dislikes = models.ManyToManyField(
        "accounts.User", related_name="disliked_posts")
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name='answers')
    post = models.ForeignKey(
        "posts.Post", on_delete=models.CASCADE, related_name='answers')
