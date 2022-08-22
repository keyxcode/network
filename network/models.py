from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser, models.Model):
    followers = models.ManyToManyField("User", blank="true", related_name="follow")
    follows = models.ManyToManyField("User", blank="true", related_name="followed_by")

    def serialize(self):
        return {
            "followers": [user.username for user in self.followers.all()],
            "follows": [user.username for user in self.follows.all()]
        }


class Post(models.Model):
    content = models.TextField(blank=True)
    poster = models.ForeignKey("User", on_delete=models.CASCADE, null=True, related_name="all_posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField("User", related_name="liked_post")

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "poster": self.poster.username,
            "timestamp": self.timestamp,
            "likers": [user.username for user in self.likers.all()]
        }
        
    def __str__(self):
        return f"{self.id}: {self.poster} - {self.content}"