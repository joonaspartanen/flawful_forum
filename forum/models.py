from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
  subject = models.CharField(max_length=100)
  body = models.CharField(max_length=1000)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
