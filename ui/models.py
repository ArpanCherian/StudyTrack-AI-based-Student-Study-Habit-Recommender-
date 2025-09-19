from django.db import models

# Create your models here.
class userdetails(models.Model):
    fullname = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=16)