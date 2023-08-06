# Generated by Django 3.2.19 on 2023-08-06 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntityType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=310)),
            ],
        ),
        migrations.CreateModel(
            name='FileResNum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=310)),
            ],
        ),
        migrations.CreateModel(
            name='MediumResType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=310)),
            ],
        ),
        migrations.CreateModel(
            name='NameType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=310)),
            ],
        ),
        migrations.CreateModel(
            name='StatusType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=310)),
            ],
        ),
        migrations.CreateModel(
            name='PqrsMain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_entry', models.DateTimeField()),
                ('sender', models.CharField(blank=True, max_length=300, null=True)),
                ('subject', models.CharField(blank=True, max_length=300, null=True)),
                ('file_num', models.CharField(blank=True, max_length=300, null=True)),
                ('days_of_the_response', models.CharField(blank=True, max_length=500, null=True)),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('date_of_response', models.DateTimeField(auto_now_add=True)),
                ('file_res', models.CharField(blank=True, max_length=300, null=True)),
                ('comment', models.CharField(blank=True, max_length=300, null=True)),
                ('pdf', models.FileField(blank=True, null=True, upload_to='pdfs/pqrs/')),
                ('entity_or_position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pqrsAPI.entitytype')),
                ('medium_of_the_response', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pqrsAPI.mediumrestype')),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pqrsAPI.nametype')),
                ('responsible_for_the_response', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Auth.team')),
                ('status_of_the_response', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pqrsAPI.statustype')),
            ],
        ),
    ]
