# Generated by Django 3.2.7 on 2021-09-14 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210913_1423'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='USERNAME_FIELD',
        ),
    ]
