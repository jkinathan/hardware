# Generated by Django 2.2.14 on 2020-09-08 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hard', '0018_auto_20200908_0740'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]