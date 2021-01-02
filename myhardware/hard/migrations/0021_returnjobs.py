# Generated by Django 2.2.14 on 2020-09-09 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hard', '0020_auto_20200909_0720'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReturnJobs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobname', models.CharField(max_length=100)),
                ('complaint', models.TextField(blank=True, max_length=200)),
                ('partnumber', models.CharField(blank=True, max_length=50)),
                ('datedone', models.DateField()),
                ('status', models.CharField(choices=[('Complete', 'Complete'), ('Incomplete', 'Incomplete')], max_length=20)),
                ('customer_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hard.Customer')),
            ],
        ),
    ]