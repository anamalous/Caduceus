# Generated by Django 5.0.2 on 2024-04-07 10:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicare', '0006_alter_appointments_date_alter_patientdata_dob_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointments',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 4, 7, 16, 22, 29, 983524)),
        ),
        migrations.AlterField(
            model_name='patientdata',
            name='dob',
            field=models.DateField(default=datetime.datetime(2024, 4, 7, 16, 22, 29, 999030)),
        ),
    ]