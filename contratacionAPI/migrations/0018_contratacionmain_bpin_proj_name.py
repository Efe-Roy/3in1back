# Generated by Django 3.2.23 on 2024-03-03 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratacionAPI', '0017_auto_20240220_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='contratacionmain',
            name='bpin_proj_name',
            field=models.CharField(blank=True, max_length=2310, null=True),
        ),
    ]
