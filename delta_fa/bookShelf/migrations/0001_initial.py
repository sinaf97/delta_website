# Generated by Django 2.1.7 on 2019-03-31 20:44

import bookShelf.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0014_auto_20190331_2036'),
    ]

    operations = [
        migrations.CreateModel(
            name='book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=60, null=True)),
                ('book_family_name', models.CharField(blank=True, max_length=60, null=True)),
                ('authors', models.CharField(blank=True, max_length=128, null=True)),
                ('publish_place', models.CharField(blank=True, max_length=64, null=True)),
                ('level', models.CharField(blank=True, max_length=32, null=True)),
                ('book_pic', models.FileField(default='default/book_pic.jpg', null=True, upload_to=bookShelf.models.book_picPath)),
                ('description', models.CharField(blank=True, max_length=512, null=True)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard.course')),
            ],
        ),
        migrations.CreateModel(
            name='date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField(null=True)),
                ('month', models.PositiveIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('day', models.PositiveIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)])),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='publish_date',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='bookShelf.date'),
        ),
    ]
