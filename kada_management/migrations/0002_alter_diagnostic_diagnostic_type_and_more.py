# Generated by Django 4.2.13 on 2024-08-11 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kada_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnostic',
            name='diagnostic_type',
            field=models.CharField(choices=[('initial', 'Initial'), ('technicien', 'Technicien'), ('final', 'Final')], max_length=20),
        ),
        migrations.AlterField(
            model_name='reparation',
            name='date_debut',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reparation',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('created', 'Created'), ('accepted', 'Accepted'), ('declined', 'Declined'), ('completed', 'Completed'), ('canceled', 'Canceled'), ('suspended', 'Suspended')], default='created', max_length=20),
        ),
    ]