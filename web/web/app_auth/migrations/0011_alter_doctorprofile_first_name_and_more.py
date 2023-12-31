# Generated by Django 4.2.3 on 2023-08-05 19:35

import django.core.validators
from django.db import migrations, models
import web.app_auth.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth', '0010_customuser_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorprofile',
            name='first_name',
            field=models.CharField(max_length=30, null=True, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='doctorprofile',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'other')], max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='doctorprofile',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, null=True, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='doctorprofile',
            name='middle_name',
            field=models.CharField(max_length=30, null=True, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='doctorprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[web.app_auth.validators.validate_only_digits, django.core.validators.MinLengthValidator(10)]),
        ),
        migrations.AlterField(
            model_name='doctorprofile',
            name='specialization',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='civil_number',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[web.app_auth.validators.validate_only_digits, django.core.validators.MinLengthValidator(10)]),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='first_name',
            field=models.CharField(max_length=30, null=True, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, null=True, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='middle_name',
            field=models.CharField(max_length=30, null=True, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[web.app_auth.validators.validate_only_digits, django.core.validators.MinLengthValidator(10)]),
        ),
    ]
