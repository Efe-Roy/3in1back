# Generated by Django 3.2.19 on 2023-12-09 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketAPI', '0006_ticket_assign_to_agent'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='feedback',
            field=models.TextField(blank=True),
        ),
    ]
