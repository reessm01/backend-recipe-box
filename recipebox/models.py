from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    bio = models.TextField()

    def __str__(self):
        return self.user.username

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    time_rq = models.IntegerField()
    instructions = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)