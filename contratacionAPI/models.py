from django.db import models
from Auth.models import UserProfile, Agent, Team, User

# Create your models here.
class ContratacionMain(models.Model):
    process = models.ForeignKey("processType", null=True, blank=True, on_delete=models.SET_NULL)
    acroyms_of_contract = models.ForeignKey("acroymsType", null=True, blank=True, on_delete=models.SET_NULL)
    typology = models.ForeignKey("typologyType", null=True, blank=True, on_delete=models.SET_NULL)
    contact_no = models.CharField(max_length=2300, null=True)
    contractor = models.CharField(max_length=2300, null=True)
    contractor_identification = models.CharField(max_length=2300, null=True)
    verification_digit = models.CharField(max_length=2300, null=True)
    birthday_date = models.DateTimeField()
    blood_type = models.CharField(max_length=2300, null=True)
    sex = models.CharField(max_length=2300, null=True)
    object = models.CharField(max_length=2300, null=True)
    worth = models.CharField(max_length=2300, null=True)
    duration = models.CharField(max_length=2300, null=True)
    contract_date = models.DateTimeField()
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    advance = models.CharField(max_length=2310)
    report_secop_begins = models.CharField(max_length=2310)
    secop_contract_report = models.CharField(max_length=2310)
    report_honest_antioquia = models.CharField(max_length=2310)
    report_institute_web = models.CharField(max_length=2310)
    sia_observe_report = models.CharField(max_length=2310)
    act_liquidation = models.CharField(max_length=2310)
    settlement_report = models.CharField(max_length=2310)
    close_record_and_report_date = models.CharField(max_length=2310)
    addition = models.CharField(max_length=2310)
    value_added = models.CharField(max_length=2310)
    extra_time = models.CharField(max_length=2310)
    bpin_project_code = models.CharField(max_length=2310)
    value_affected_bpin_proj_cdp = models.CharField(max_length=2310)
    budget_items = models.CharField(max_length=2310)
    article_name = models.CharField(max_length=2310)
    item_value = models.CharField(max_length=2310)
    state = models.ForeignKey("StateType", null=True, blank=True, on_delete=models.SET_NULL)
    responsible_secretary = models.ForeignKey("resSecType", null=True, blank=True, on_delete=models.SET_NULL)
    name_supervisor_or_controller = models.CharField(max_length=2310)
    observations = models.CharField(max_length=2310)
    contract_value_plus = models.CharField(max_length=2310)
    real_executed_value_according_to_settlement = models.CharField(max_length=2310)
    file_status = models.CharField(max_length=2310)


class processType(models.Model):
    name = models.CharField(max_length=310)

    def __str__(self):
        return self.name

class acroymsType(models.Model):
    name = models.CharField(max_length=310)

    def __str__(self):
        return self.name

class typologyType(models.Model):
    name = models.CharField(max_length=310)

    def __str__(self):
        return self.name

class resSecType(models.Model):
    name = models.CharField(max_length=310)

    def __str__(self):
        return self.name

class StateType(models.Model):
    name = models.CharField(max_length=310)

    def __str__(self):
        return self.name
