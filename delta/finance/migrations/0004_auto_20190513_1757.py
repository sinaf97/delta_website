# Generated by Django 2.1.7 on 2019-05-13 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_auto_20190513_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='account_number',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='invoices', to='dashboard.CourseInfo'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='receipt', to='dashboard.CourseInfo'),
        ),
    ]