# Generated by Django 4.2.3 on 2023-07-17 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth', '0005_alter_doctorprofile_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='for_time',
            field=models.TimeField(choices=[('09:00 AM', '09:00 AM'), ('09:30 AM', '09:30 AM'), ('10:00 AM', '10:00 AM'), ('10:30 AM', '10:30 AM'), ('11:00 AM', '11:00 AM'), ('11:30 AM', '11:30 AM'), ('12:00 PM', '12:00 PM'), ('12:30 PM', '12:30 PM'), ('01:00 PM', '01:00 PM'), ('01:30 PM', '01:30 PM'), ('02:00 PM', '02:00 PM'), ('02:30 PM', '02:30 PM'), ('03:00 PM', '03:00 PM'), ('03:30 PM', '03:30 PM'), ('04:00 PM', '04:00 PM')]),
        ),
    ]