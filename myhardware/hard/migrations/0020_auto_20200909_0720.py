# Generated by Django 2.2.14 on 2020-09-09 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hard', '0019_customer_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date',
            field=models.DateField(default='2020-09-09'),
        ),
        migrations.AlterField(
            model_name='technician',
            name='date',
            field=models.DateField(default='2020-09-09'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='date',
            field=models.DateField(default='2020-09-09'),
        ),
    ]
