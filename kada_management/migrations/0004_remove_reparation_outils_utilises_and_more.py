# Generated by Django 4.2.13 on 2024-07-06 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kada_management', '0003_client_created_time_client_updated_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reparation',
            name='outils_utilises',
        ),
        migrations.RemoveField(
            model_name='reparation',
            name='pannes',
        ),
    ]
