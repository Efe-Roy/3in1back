# Generated by Django 3.2.19 on 2023-08-10 19:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UrbanControl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filed', models.CharField(max_length=2300, null=True)),
                ('date_received', models.DateTimeField(blank=True, null=True)),
                ('Involved_applicant', models.CharField(max_length=2300, null=True)),
                ('res_report', models.CharField(max_length=2300, null=True)),
                ('comment', models.CharField(blank=True, max_length=2300, null=True)),
                ('file_res', models.CharField(blank=True, max_length=2300, null=True)),
                ('pdf', models.FileField(blank=True, null=True, upload_to='pdfs/urbancontrol/')),
                ('assign_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Auth.team')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TrafficViolationComparedMyColission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_received', models.DateTimeField(blank=True, null=True)),
                ('involved', models.CharField(max_length=2300, null=True)),
                ('res_procedure', models.CharField(max_length=2300, null=True)),
                ('comment', models.CharField(blank=True, max_length=2300, null=True)),
                ('file_res', models.CharField(blank=True, max_length=2300, null=True)),
                ('pdf', models.FileField(blank=True, null=True, upload_to='pdfs/TrafficViolationComparedMyColission/')),
                ('assign_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Auth.team')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TrafficViolationCompared',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_events', models.DateTimeField(blank=True, null=True)),
                ('date_received', models.DateTimeField(blank=True, null=True)),
                ('involved', models.CharField(max_length=2300, null=True)),
                ('id_card', models.CharField(max_length=2300, null=True)),
                ('violation_code', models.CharField(max_length=2300, null=True)),
                ('res_procedure', models.CharField(max_length=2300, null=True)),
                ('comment', models.CharField(blank=True, max_length=2300, null=True)),
                ('file_res', models.CharField(blank=True, max_length=2300, null=True)),
                ('pdf', models.FileField(blank=True, null=True, upload_to='pdfs/TrafficViolationCompared/')),
                ('assign_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Auth.team')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PoliceSubmissionLGGS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2300, null=True)),
                ('Id_card', models.CharField(max_length=2300, null=True)),
                ('appearance_num', models.CharField(max_length=2300, null=True)),
                ('act_num', models.CharField(max_length=2300, null=True)),
                ('comment', models.CharField(blank=True, max_length=2300, null=True)),
                ('file_res', models.CharField(blank=True, max_length=2300, null=True)),
                ('pdf', models.FileField(blank=True, null=True, upload_to='pdfs/PoliceSubmissionLGGS/')),
                ('assign_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Auth.team')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PoliceCompliant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filed', models.CharField(max_length=2300, null=True)),
                ('date_received', models.DateTimeField(blank=True, null=True)),
                ('complainants', models.CharField(max_length=2300, null=True)),
                ('defendants', models.CharField(max_length=2300, null=True)),
                ('comment', models.CharField(blank=True, max_length=2300, null=True)),
                ('file_res', models.CharField(blank=True, max_length=2300, null=True)),
                ('pdf', models.FileField(blank=True, null=True, upload_to='pdfs/PoliceCompliant/')),
                ('assign_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Auth.team')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='File2Return2dOffice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filed', models.CharField(max_length=2300, null=True)),
                ('guy', models.DateTimeField(blank=True, null=True)),
                ('involved', models.CharField(max_length=2300, null=True)),
                ('comment', models.CharField(blank=True, max_length=2300, null=True)),
                ('file_res', models.CharField(blank=True, max_length=2300, null=True)),
                ('pdf', models.FileField(blank=True, null=True, upload_to='pdfs/File2Return2dOffice/')),
                ('assign_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Auth.team')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ComplaintAndOfficeToAttend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filed', models.CharField(max_length=2300, null=True)),
                ('date_received', models.DateTimeField(blank=True, null=True)),
                ('affair', models.CharField(max_length=2300, null=True)),
                ('comment', models.CharField(blank=True, max_length=2300, null=True)),
                ('file_res', models.CharField(blank=True, max_length=2300, null=True)),
                ('pdf', models.FileField(blank=True, null=True, upload_to='pdfs/ComplaintAndOfficeToAttend/')),
                ('assign_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Auth.team')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
