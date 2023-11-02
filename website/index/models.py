from django.db import models
from django.contrib.auth.models import User

# Create your models here
class User(User):
    is_member = models.BooleanField(default=False)
    def serialize(self):
        return {
            "username": self.username,
            "email": self.email
        }

class Question(models.Model):
    time = models.DateTimeField(auto_now=False, auto_now_add=True)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=1000)
    def serialize(self):
        return {
            "pk": self.id,
            "time": self.time,
            "title": self.title,
            "content": self.content
        }

class Comment(models.Model):
    time = models.DateTimeField(auto_now=True, auto_now_add=False)
    question = models.IntegerField()
    content = models.CharField(max_length=10000)
    user = models.IntegerField()
    votes = models.IntegerField(default=0)

class Vote(models.Model):
    user = models.IntegerField()
    comment = models.IntegerField()