# Generated by Django 3.2.19 on 2023-09-22 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InspecciónAPI', '0008_uploadsignedpdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaintandofficetoattend',
            name='status_track',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='file2return2doffice',
            name='status_track',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='policecompliant',
            name='status_track',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='policesubmissionlggs',
            name='status_track',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='trafficviolationcompared',
            name='status_track',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='trafficviolationcomparedmycolission',
            name='status_track',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='urbancontrol',
            name='status_track',
            field=models.BooleanField(default=False),
        ),
    ]
