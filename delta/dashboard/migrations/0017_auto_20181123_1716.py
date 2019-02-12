# Generated by Django 2.1 on 2018-11-23 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_auto_20181123_1711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='term',
            name='course',
        ),
        migrations.RemoveField(
            model_name='term',
            name='students',
        ),
        migrations.AddField(
            model_name='term',
            name='part',
            field=models.DecimalField(decimal_places=0, max_digits=1, null=True),
        ),
        migrations.AddField(
            model_name='term',
            name='season',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='term',
            name='year',
            field=models.DecimalField(decimal_places=0, max_digits=4, null=True),
        ),
    ]
