from django.db import models


class Answer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    likes = models.IntegerField(default=0)
    deslikes = models.IntegerField(default=0)
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name='answers')
    post = models.ForeignKey(
        "posts.Post", on_delete=models.CASCADE, related_name='answers')
