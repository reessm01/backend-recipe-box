from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=30)
    bio = models.TextField()

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    time_rq = models.IntegerField()
    instructions = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
