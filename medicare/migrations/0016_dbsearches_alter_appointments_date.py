# Generated by Django 5.0.2 on 2024-04-07 19:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicare', '0015_delete_visitlog_currentadmits_currentdiagnosis_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DBsearches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scan', models.ImageField(default='hello.jpg', upload_to='media')),
            ],
        ),
        migrations.AlterField(
            model_name='appointments',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 4, 8, 0, 47, 42, 216284)),
        ),
    ]
