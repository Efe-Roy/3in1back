# Generated by Django 3.2.19 on 2023-10-14 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0006_user_approve_signature'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_hiring_org',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_sisben',
            field=models.BooleanField(default=False),
        ),
    ]