# Generated by Django 2.1.7 on 2019-05-13 11:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0022_auto_20190509_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='courseInfo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='courses', to='dashboard.CourseInfo'),
        ),
        migrations.AlterField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='courses', to='dashboard.Teacher'),
        ),
        migrations.AlterField(
            model_name='course',
            name='term',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='dashboard.Term'),
        ),
        migrations.AlterField(
            model_name='courseinfo',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='courses', to='bookShelf.Book'),
        ),
        migrations.AlterField(
            model_name='massege',
            name='origin',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_masseges', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='massege',
            name='to',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recieved_masseges', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='score',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='dashboard.Course'),
        ),
        migrations.AlterField(
            model_name='score',
            name='student',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='dashboard.Student'),
        ),
        migrations.AlterField(
            model_name='student',
            name='course',
            field=models.ManyToManyField(related_name='students', to='dashboard.Course'),
        ),
    ]