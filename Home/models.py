# models.py
from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission


    



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
    



class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='led_teams')
    members = models.ManyToManyField(User, related_name='joined_teams', blank=True)

    def __str__(self):
        return self.name

class TeamRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ]
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.team.name} ({self.status})"




class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    # location = models.CharField(max_length=255, blank=True, null=True)   # Event venue/location
    # organizer = models.CharField(max_length=255, blank=True, null=True)  # Organizer name or organization
    # created_at = models.DateTimeField(auto_now_add=True)                 # Timestamp of creation
    # updated_at = models.DateTimeField(auto_now=True)                     # Timestamp of last update

    def __str__(self):
        return self.name


class TeamJoinRequest(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='join_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(null=True, blank=True)  # None = Pending, True = Accepted, False = Rejected
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.team.name}"