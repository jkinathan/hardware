# Generated by Django 2.2.14 on 2020-09-03 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hard', '0012_auto_20200903_0704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
