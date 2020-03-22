from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save  # perform action before save

from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    timestamp = models.DateTimeField(auto_now=True)
    liked_users = models.ManyToManyField(User, related_name='liked_users')

    def __str__(self):
        return f"{self.id}. {self.title}"

    class Meta:
        ordering = ["-timestamp", ]


