# Generated by Django 3.2.23 on 2024-02-01 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InspecciónAPI', '0017_auto_20240130_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='filterselection',
            name='pdf_fn1',
            field=models.FileField(blank=True, null=True, upload_to='pdfs/AUTO_DE_REPARTO_pdfs/'),
        ),
        migrations.AddField(
            model_name='filterselection',
            name='pdf_fn2',
            field=models.FileField(blank=True, null=True, upload_to='pdfs/NOTIFICACIÓN_pdfs/'),
        ),
    ]
