from django.db import models
from django.contrib.auth.models import User

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who owns the bookmark
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=200)
    added_time = models.DateTimeField(auto_now_add=True)

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title