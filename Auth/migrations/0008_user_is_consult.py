# Generated by Django 3.2.19 on 2023-11-02 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0007_auto_20231014_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_consult',
            field=models.BooleanField(default=False),
        ),
    ]