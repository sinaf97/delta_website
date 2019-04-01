# Generated by Django 2.1.7 on 2019-04-01 15:46

import bookShelf.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookShelf', '0003_remove_book_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='bookGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(blank=True, max_length=60, null=True)),
                ('group_pic', models.FileField(default='default/book_pic.jpg', null=True, upload_to=bookShelf.models.book_group_picPath)),
            ],
        ),
        migrations.RemoveField(
            model_name='book',
            name='book_family_name',
        ),
        migrations.AddField(
            model_name='book',
            name='book_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bookShelf.bookGroup'),
        ),
    ]
