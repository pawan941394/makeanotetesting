# Generated by Django 3.2.7 on 2021-09-14 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_userprofile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='instagram',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='linkedin',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(default='', max_length=15),
        ),
    ]
