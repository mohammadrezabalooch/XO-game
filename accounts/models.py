from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    wins = models.PositiveSmallIntegerField()
    loses = models.PositiveSmallIntegerField()
    draws = models.PositiveSmallIntegerField()
