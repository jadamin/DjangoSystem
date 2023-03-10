# Generated by Django 4.1.5 on 2023-02-06 08:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BetterYou', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointement',
            name='day',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='appointement',
            name='service',
            field=models.CharField(choices=[('Web Developpement', 'Web Developpement'), ('AI Developpement', 'AI Developpement')], default='AI Developpement ', max_length=100),
        ),
        migrations.AddField(
            model_name='appointement',
            name='time',
            field=models.CharField(choices=[('09:00 AM ', '09:00 AM '), ('09:40 AM ', '09:40 AM '), ('10:20 AM ', '10:20 AM '), ('11:40 AM ', '11:40 AM '), ('13:30 PM ', '13:30 PM '), ('14:10 PM ', '14:10 PM '), ('14:50 PM ', '14:50 PM '), ('15:30 pm ', '15:30 pm '), ('16:10 pm ', '16:10 pm '), ('16:50 pm ', '16:50 pm ')], default='09:00 AM', max_length=30),
        ),
        migrations.AddField(
            model_name='appointement',
            name='time_ordered',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
