# Generated by Django 3.2.19 on 2023-12-05 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratacionAPI', '0004_alter_contratacionmain_value_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valueadded',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
