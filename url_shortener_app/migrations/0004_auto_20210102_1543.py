# Generated by Django 3.1.4 on 2021-01-02 10:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('url_shortener_app', '0003_auto_20210101_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlocation',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userlocation',
            name='ip',
            field=models.CharField(default=123, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userlocation',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userlocation',
            name='lat',
            field=models.DecimalField(decimal_places=5, max_digits=8),
        ),
        migrations.AlterField(
            model_name='userlocation',
            name='long',
            field=models.DecimalField(decimal_places=5, max_digits=8),
        ),
    ]