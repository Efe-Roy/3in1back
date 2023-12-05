# Generated by Django 3.2.19 on 2023-12-02 22:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contratacionAPI', '0003_auto_20231121_0623'),
        ('ticketAPI', '0002_ticket_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='responsible_secretary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contratacionAPI.ressectype'),
        ),
    ]