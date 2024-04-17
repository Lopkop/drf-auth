import uuid

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255, default='')
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)


class RefreshToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    refresh_token = models.UUIDField(default=uuid.uuid4)
    expires = models.DateTimeField()
