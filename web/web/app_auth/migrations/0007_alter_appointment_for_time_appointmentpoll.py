# Generated by Django 4.2.3 on 2023-07-18 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth', '0006_alter_appointment_for_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='for_time',
            field=models.CharField(choices=[('09:00 AM', '09:00 AM'), ('09:30 AM', '09:30 AM'), ('10:00 AM', '10:00 AM'), ('10:30 AM', '10:30 AM'), ('11:00 AM', '11:00 AM'), ('11:30 AM', '11:30 AM'), ('12:00 PM', '12:00 PM'), ('12:30 PM', '12:30 PM'), ('13:00 PM', '01:00 PM')]),
        ),
        migrations.CreateModel(
            name='AppointmentPoll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_condition', models.CharField(choices=[('Excellent', 'Excellent'), ('Good', 'Good'), ('Not feeling very well', 'Not feeling very well')])),
                ('high_temperature', models.BooleanField()),
                ('cough', models.BooleanField()),
                ('sores_in_mouth', models.BooleanField()),
                ('sores_in_nose', models.BooleanField()),
                ('cold', models.BooleanField()),
                ('diarrhea', models.BooleanField()),
                ('skin_rash', models.BooleanField()),
                ('additional_info', models.TextField(blank=True, null=True)),
                ('appointment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app_auth.appointment')),
            ],
        ),
    ]
