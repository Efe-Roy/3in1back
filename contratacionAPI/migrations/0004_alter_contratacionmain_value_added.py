# Generated by Django 3.2.19 on 2023-12-05 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratacionAPI', '0003_auto_20231121_0623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contratacionmain',
            name='value_added',
            field=models.ManyToManyField(blank=True, null=True, to='contratacionAPI.ValueAdded'),
        ),
    ]
