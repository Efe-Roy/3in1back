# Generated by Django 3.2.19 on 2023-07-28 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratacionAPI', '0003_auto_20230728_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='contratacionmain',
            name='url_1',
            field=models.CharField(blank=True, max_length=2310, null=True),
        ),
        migrations.AddField(
            model_name='contratacionmain',
            name='url_2',
            field=models.CharField(blank=True, max_length=2310, null=True),
        ),
    ]
