# Generated by Django 2.0.1 on 2018-01-20 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0002_auto_20180120_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='attemtps',
            field=models.IntegerField(default=0, help_text='Total of exam trials'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='examScore',
            field=models.IntegerField(default=0, help_text='Total score of the exam'),
        ),
    ]
