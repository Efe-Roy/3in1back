# Generated by Django 3.2.23 on 2024-01-18 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pqrsAPI', '0004_auto_20240110_0039'),
    ]

    operations = [
        migrations.AddField(
            model_name='pqrsmain',
            name='need_answer',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]