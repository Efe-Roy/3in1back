# Generated by Django 3.2.19 on 2023-09-21 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0005_alter_user_signature'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='approve_signature',
            field=models.BooleanField(default=False),
        ),
    ]
