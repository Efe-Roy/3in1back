# Generated by Django 3.2.19 on 2023-12-06 09:16

from django.db import migrations, models
import ticketAPI.models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketAPI', '0004_remove_ticket_responsible_secretary'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=ticketAPI.models.upload_to, verbose_name='Image'),
        ),
    ]
