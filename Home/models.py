# models.py
from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.BigIntegerField(null=True, blank=True)
    class_name = models.CharField(max_length=20)
    section = models.CharField(max_length=5)
    roll_number = models.CharField(max_length=10)
    linkedin_url = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    about = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CollegeProfile(models.Model):
    name = models.CharField(max_length=122)
    address = models.CharField(max_length=244)
    



# added today

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=50)
    section = models.CharField(max_length=10)
    net_number = models.CharField(max_length=20)
    about_you = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    virtues = models.ManyToManyField('Virtue')
    

class Virtue(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name