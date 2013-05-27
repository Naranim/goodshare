from django.db import models
from django.contrib.auth.models import ( BaseUserManager, AbstractBaseUser )


class UserManager(BaseUserManager):
    pass


class Account(AbstractBaseUser):
    pass


class Comment(models.Model):
    pass


class Rate(models.Model):
    pass


class Transaction(models.Model):
    pass
