# Generated by Django 4.2.13 on 2024-07-07 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kada_management', '0004_remove_reparation_outils_utilises_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reparation',
            name='numero_reparation',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]
