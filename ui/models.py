from django.db import models

# Create your models here.
class userdetails(models.Model):
    fullname = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=16)


class admindetails(models.Model):
    adminfullname = models.CharField(max_length=30)
    adminemail = models.EmailField(max_length=30)
    adminusername = models.CharField(max_length=20)
    adminpassword = models.CharField(max_length=16)


class studentdetails(models.Model):
    studentname = models.CharField(max_length=30)
    coursename = models.CharField(max_length=30)
    startdate = models.DateField()
    enddate = models.DateField()
    hoursspent = models.FloatField()  # since you allow decimal like 12.5
    completion = models.IntegerField()  # percentage (0–100)
    status = models.CharField(
        max_length=20,
        choices=[('Ongoing', 'Ongoing'),
                 ('Completed', 'Completed'),
                 ('Not Started', 'Not Started')]
    )