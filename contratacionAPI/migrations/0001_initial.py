# Generated by Django 3.2.19 on 2023-07-27 21:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='acroymsType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=310, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='BpinProjectCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='BudgetItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ItemValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='processType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=310, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='resSecType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=310, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StateType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=310, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='typologyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=310, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ValueAdded',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ValueAffectedBpinProjCDP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ContratacionMain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_num', models.CharField(blank=True, max_length=2300, null=True)),
                ('contact_no', models.CharField(blank=True, max_length=2300, null=True)),
                ('contractor', models.CharField(blank=True, max_length=2300, null=True)),
                ('contractor_identification', models.CharField(blank=True, max_length=2300, null=True)),
                ('verification_digit', models.CharField(blank=True, max_length=2300, null=True)),
                ('birthday_date', models.DateField(blank=True, null=True)),
                ('blood_type', models.CharField(blank=True, max_length=2300, null=True)),
                ('sex', models.CharField(blank=True, max_length=2300, null=True)),
                ('object', models.CharField(blank=True, max_length=2300, null=True)),
                ('worth', models.CharField(blank=True, max_length=2300, null=True)),
                ('duration', models.CharField(blank=True, max_length=2300, null=True)),
                ('contract_date', models.DateField(blank=True, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('finish_date', models.DateField(blank=True, null=True)),
                ('advance', models.CharField(blank=True, max_length=2310, null=True)),
                ('report_secop_begins', models.DateField(blank=True, null=True)),
                ('secop_contract_report', models.DateField(blank=True, null=True)),
                ('report_honest_antioquia', models.DateField(blank=True, null=True)),
                ('report_institute_web', models.DateField(blank=True, null=True)),
                ('transparent_management_report', models.DateField(blank=True, null=True)),
                ('act_liquidation', models.DateField(blank=True, null=True)),
                ('settlement_report', models.CharField(blank=True, max_length=2310, null=True)),
                ('close_record_and_report_date', models.CharField(blank=True, max_length=2310, null=True)),
                ('addition', models.CharField(blank=True, max_length=2310, null=True)),
                ('extra_time', models.CharField(blank=True, max_length=2310, null=True)),
                ('name_supervisor_or_controller', models.CharField(blank=True, max_length=2310, null=True)),
                ('observations', models.CharField(blank=True, max_length=2310, null=True)),
                ('contract_value_plus', models.CharField(blank=True, max_length=2310, null=True)),
                ('real_executed_value_according_to_settlement', models.CharField(blank=True, max_length=2310, null=True)),
                ('file_status', models.CharField(blank=True, max_length=2310, null=True)),
                ('acroyms_of_contract', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contratacionAPI.acroymstype')),
                ('article_name', models.ManyToManyField(to='contratacionAPI.ArticleName')),
                ('bpin_project_code', models.ManyToManyField(to='contratacionAPI.BpinProjectCode')),
                ('budget_items', models.ManyToManyField(to='contratacionAPI.BudgetItems')),
                ('item_value', models.ManyToManyField(to='contratacionAPI.ItemValue')),
                ('process', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contratacionAPI.processtype')),
                ('responsible_secretary', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contratacionAPI.ressectype')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contratacionAPI.statetype')),
                ('typology', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contratacionAPI.typologytype')),
                ('value_added', models.ManyToManyField(to='contratacionAPI.ValueAdded')),
                ('value_affected_bpin_proj_cdp', models.ManyToManyField(to='contratacionAPI.ValueAffectedBpinProjCDP')),
            ],
        ),
    ]
