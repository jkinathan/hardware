# Generated by Django 2.2.14 on 2020-09-03 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hard', '0008_inventory_cut'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='updated_at',
        ),
    ]
