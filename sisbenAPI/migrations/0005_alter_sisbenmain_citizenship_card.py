# Generated by Django 3.2.23 on 2024-01-30 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sisbenAPI', '0004_auto_20230930_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sisbenmain',
            name='citizenship_card',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
