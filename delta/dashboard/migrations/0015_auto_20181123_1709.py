# Generated by Django 2.1 on 2018-11-23 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_auto_20181123_1708'),
    ]

    operations = [
        migrations.RenameField(
            model_name='score',
            old_name='score',
            new_name='scorenum',
        ),
    ]
