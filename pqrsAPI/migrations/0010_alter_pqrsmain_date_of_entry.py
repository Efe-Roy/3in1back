# Generated by Django 3.2.23 on 2024-05-14 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pqrsAPI', '0009_pqrsmain_pdf_res'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pqrsmain',
            name='date_of_entry',
            field=models.DateField(blank=True, null=True),
        ),
    ]
