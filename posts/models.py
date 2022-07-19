from django.db import models
import uuid


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    usefull_post = models.ManyToManyField(
        "accounts.User", related_name="usefull_posts")
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="posts")
    tags = models.ManyToManyField("tags.Tag", related_name="posts")
