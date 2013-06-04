from django.db import models


class Type(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return self.name


class Good(models.Model):
    name = models.CharField(max_length=35)
    type = models.ForeignKey(Type)
    description = models.TextField()

    def __unicode__(self):
        return self.name
