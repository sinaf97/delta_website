# Generated by Django 2.1.7 on 2019-05-13 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookShelf', '0007_auto_20190403_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bookShelf.BookGroup'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publish_date',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='bookShelf.Date'),
        ),
    ]
