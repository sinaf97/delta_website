# Generated by Django 2.1 on 2018-11-23 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_score_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='score',
            name='name',
        ),
    ]
