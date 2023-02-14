from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django import forms



from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

SERVICE_CHOICES = (
    ("Web Development", "Web Development"),
    ("APP Development", "APP Development"),
    ("AI Development","AI Development"),
    )
TIME_CHOICES = [
    ("09:00 ","09:00 "),
    ("09:40 ","09:40 "),
    ("10:20 ","10:20 "),
    ("11:40 ","11:40 "),
    ("13:30 ","13:30 "),
    ("14:10 ","14:10 "),
    ("14:50 ","14:50 "),
    ("15:30 ","15:30 "),
    ("16:10 ","16:10 "),
    ("16:50 ","16:50 ")
]

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, default="AI Development")
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="09:00")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return f"{self.user.username} | day: {self.day} | time: {self.time}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
  
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publication_date = models.DateField()

    def __str__(self):
        return self.title


class PasswordVerificationForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


 