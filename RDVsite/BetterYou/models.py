from django.db import models
from datetime import datetime
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin ,User
from django.db import models
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin,models.Model):
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='custom_user',
    )
    ...




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