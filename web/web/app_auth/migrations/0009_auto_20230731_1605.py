# Generated by Django 4.2.3 on 2023-07-31 13:05

from django.db import migrations


def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.create(name='Doctors')
    Group.objects.create(name='Patients')


class Migration(migrations.Migration):
    dependencies = [
        ('app_auth', '0008_medication_therapyplan'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]