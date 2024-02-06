# Generated by Django 3.2.19 on 2023-09-18 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0003_user_position'),
        ('InspecciónAPI', '0007_policesubmissionlggs_type_of_identification'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadSignedPDF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_num', models.CharField(max_length=310)),
                ('pdf', models.FileField(blank=True, null=True, upload_to='pdfs/SignedPDF/')),
                ('createdAt', models.DateField(auto_now_add=True)),
                ('assign_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Auth.agent')),
            ],
        ),
    ]
