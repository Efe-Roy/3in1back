# Generated by Django 3.2.19 on 2023-07-10 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pqrsAPI', '0004_pqrsmain_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pqrsmain',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='pdfs/pqrs/'),
        ),
    ]
