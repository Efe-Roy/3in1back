# Generated by Django 3.2.19 on 2023-12-09 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketAPI', '0007_ticket_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='ticket_num',
            field=models.CharField(default=None, max_length=30, null=True, blank=True),
        ),
    ]
