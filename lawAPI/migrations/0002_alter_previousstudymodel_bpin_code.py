# Generated by Django 3.2.23 on 2024-01-25 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lawAPI', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='previousstudymodel',
            name='bpin_code',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
