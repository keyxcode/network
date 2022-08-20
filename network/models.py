from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=256)
    poster = models.ForeignKey("User", on_delete=models.CASCADE, null=True, related_name="all_posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField("User", related_name="liked_post")

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "poster": self.poster,
            "timestamp": self.timestamp,
            "likers": [user.username for user in self.likers.all()]
        }
    def __str__(self):
        return f"{self.id}: {self.poster} - {self.content}"