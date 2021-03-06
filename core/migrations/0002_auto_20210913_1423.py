# Generated by Django 3.2.7 on 2021-09-13 08:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='USERNAME_FIELD',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
    ]
