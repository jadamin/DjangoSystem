from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django import forms



SERVICE_CHOICES = [("Web Developpement", "Web Developpement"), ( "AI Developpement"
,  "AI Developpement"
)]


TIME_CHOICES = [
    ("09:00 AM ","09:00 AM "),
    ("09:40 AM ","09:40 AM "),
    ("10:20 AM ","10:20 AM "),
    ("11:40 AM ","11:40 AM "),
    ("13:30 PM ","13:30 PM "),
    ("14:10 PM ","14:10 PM "),
    ("14:50 PM ","14:50 PM "),
    ("15:30 pm ","15:30 pm "),
    ("16:10 pm ","16:10 pm "),
    ("16:50 pm ","16:50 pm ")
]



class Appointement(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    service = models.CharField(max_length=100,choices=SERVICE_CHOICES,default="AI Developpement ")
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=30,choices=TIME_CHOICES,default="09:00 AM")
    time_ordered = models.DateTimeField(default=datetime.now,blank=True)

    def __str__(self) -> str:
        return f"{self.user.username} | day: {self.day} | time: {self.time}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
