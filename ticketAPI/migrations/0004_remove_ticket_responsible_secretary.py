# Generated by Django 3.2.19 on 2023-12-06 00:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketAPI', '0003_ticket_responsible_secretary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='responsible_secretary',
        ),
    ]