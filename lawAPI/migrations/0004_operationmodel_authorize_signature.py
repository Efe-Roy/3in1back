# Generated by Django 3.2.23 on 2024-05-02 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lawAPI', '0003_operationmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='operationmodel',
            name='authorize_signature',
            field=models.BooleanField(default=False),
        ),
    ]