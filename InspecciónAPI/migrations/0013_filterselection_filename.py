# Generated by Django 3.2.19 on 2023-10-18 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InspecciónAPI', '0012_filterselection'),
    ]

    operations = [
        migrations.AddField(
            model_name='filterselection',
            name='filename',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
