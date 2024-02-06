# Generated by Django 3.2.23 on 2024-01-12 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contratacionAPI', '0007_lawfirmmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='lawfirmmodel',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contratacion', to='contratacionAPI.contratacionmain'),
        ),
    ]
