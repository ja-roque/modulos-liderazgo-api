# Generated by Django 2.0.1 on 2018-01-20 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_auto_20180120_1841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='examID',
        ),
    ]