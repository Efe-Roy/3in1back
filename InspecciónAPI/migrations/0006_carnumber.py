# Generated by Django 3.2.19 on 2023-09-08 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InspecciónAPI', '0005_inspnotifify'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=310)),
            ],
        ),
    ]
