from django.db import models


class Place(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    link = models.CharField(max_length=200)
