# Generated by Django 4.1.6 on 2023-02-14 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BetterYou', '0015_alter_appointment_day_alter_appointment_service_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.TimeField(choices=[('09:00:00', '09:00 AM'), ('09:40:00', '09:40 AM'), ('10:20:00', '10:20 AM'), ('11:40:00', '11:40 AM'), ('13:30:00', '01:30 PM'), ('14:10:00', '02:10 PM'), ('14:50:00', '02:50 PM'), ('15:30:00', '03:30 pm'), ('16:10:00', '04:10 pm'), ('16:50:00', '04:50 pm')], default='09:00 AM', max_length=30),
        ),
    ]
