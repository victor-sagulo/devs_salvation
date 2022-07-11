from tkinter import CASCADE
from django.db import models

# Create your models here.
class Post(models.model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    usefull_post = models.IntegerField()
    user_id = models.ForeignKey("account.User", on_delete=CASCADE, related_name="post")
    tag_id = models.ManyToManyField("tags.Tag", related_name="post")
