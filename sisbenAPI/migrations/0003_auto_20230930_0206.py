# Generated by Django 3.2.19 on 2023-09-30 01:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sisbenAPI', '0002_auto_20230930_0058'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=310)),
            ],
        ),
        migrations.AddField(
            model_name='sisbenmain',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sisbenAPI.locationtype'),
        ),
    ]
