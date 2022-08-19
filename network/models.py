from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.person.username,
            "poster_id": self.person.id,
            "body": self.content,
            "time": self.time.strftime("%Y-%m-%d %H:%M:%S"),
            "likes": self.likes
        }

class Like(models.Model):
    person_id = models.IntegerField()
    post_id = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

class Follower(models.Model):
    influencer_id = models.IntegerField()
    influencer_name = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True)
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    def serialize(self):
        return {
            "id": self.id,
            "influencer_id": self.influencer_id,
            "influencer_name": self.influencer_name,
        }
    

