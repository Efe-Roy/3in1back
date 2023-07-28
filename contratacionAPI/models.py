from django.db import models
from Auth.models import UserProfile, Agent, Team, User

# Create your models here.
class ValueAdded(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name or ''

class BpinProjectCode(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name or ''

class ValueAffectedBpinProjCDP(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name or ''

class BudgetItems(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name or ''

class ArticleName(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name or ''

class ItemValue(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name or ''
    
class ContratacionMain(models.Model):
    process = models.ForeignKey("processType", null=True, blank=True, on_delete=models.SET_NULL)
    process_num = models.CharField(max_length=2300, null=True, blank=True)
    acroyms_of_contract = models.ForeignKey("acroymsType", null=True, blank=True, on_delete=models.SET_NULL)
    typology = models.ForeignKey("typologyType", null=True, blank=True, on_delete=models.SET_NULL)
    contact_no = models.CharField(max_length=2300, null=True, blank=True)
    contractor = models.CharField(max_length=2300, null=True, blank=True)
    contractor_identification = models.CharField(max_length=2300, null=True, blank=True)
    verification_digit = models.CharField(max_length=2300, null=True, blank=True)
    birthday_date = models.DateField(null=True, blank=True)
    blood_type = models.CharField(max_length=2300, null=True, blank=True)
    sex = models.CharField(max_length=2300, null=True, blank=True)
    object = models.CharField(max_length=2300, null=True, blank=True)
    worth = models.CharField(max_length=2300, null=True, blank=True)
    duration = models.CharField(max_length=2300, null=True, blank=True)
    contract_date = models.DateField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    finish_date = models.DateField(null=True, blank=True)
    advance = models.CharField(max_length=2310, null=True, blank=True)
    report_secop_begins = models.DateField(null=True, blank=True)
    secop_contract_report = models.DateField(null=True, blank=True)
    report_honest_antioquia = models.DateField(null=True, blank=True)
    report_institute_web = models.DateField(null=True, blank=True)
    sia_observe_report = models.DateField(null=True, blank=True)
    act_liquidation = models.DateField(null=True, blank=True)
    settlement_report = models.DateField(null=True, blank=True)
    close_record = models.DateField(null=True, blank=True)
    report_date = models.DateField(null=True, blank=True)
    addition = models.CharField(max_length=2310, null=True, blank=True)

    # value_added = models.CharField(max_length=2310, null=True, blank=True)
    value_added = models.ManyToManyField(ValueAdded)

    extra_time = models.CharField(max_length=2310, null=True, blank=True)
    # bpin_project_code = models.CharField(max_length=2310, null=True, blank=True)
    bpin_project_code = models.ManyToManyField(BpinProjectCode)

    # value_affected_bpin_proj_cdp = models.CharField(max_length=2310, null=True, blank=True)
    value_affected_bpin_proj_cdp = models.ManyToManyField(ValueAffectedBpinProjCDP)

    # budget_items = models.CharField(max_length=2310, null=True, blank=True)
    budget_items = models.ManyToManyField(BudgetItems)

    # article_name = models.CharField(max_length=2310, null=True, blank=True)
    article_name = models.ManyToManyField(ArticleName)

    # item_value = models.CharField(max_length=2310, null=True, blank=True)
    item_value = models.ManyToManyField(ItemValue)

    state = models.ForeignKey("StateType", null=True, blank=True, on_delete=models.SET_NULL)
    responsible_secretary = models.ForeignKey("resSecType", null=True, blank=True, on_delete=models.SET_NULL)
    name_supervisor_or_controller = models.CharField(max_length=2310, null=True, blank=True)
    observations = models.CharField(max_length=2310, null=True, blank=True)
    contract_value_plus = models.CharField(max_length=2310, null=True, blank=True)
    real_executed_value_according_to_settlement = models.CharField(max_length=2310, null=True, blank=True)
    file_status = models.CharField(max_length=2310, null=True, blank=True)

    def __str__(self):
        return str(self.contractor) or ''

class processType(models.Model):
    name = models.CharField(max_length=310, null=True, blank=True)

    def __str__(self):
        return str(self.name) or ''

class acroymsType(models.Model):
    name = models.CharField(max_length=310, null=True, blank=True)

    def __str__(self):
        return str(self.name) or ''

class typologyType(models.Model):
    name = models.CharField(max_length=310, null=True, blank=True)

    def __str__(self):
        return str(self.name) or ''

class resSecType(models.Model):
    name = models.CharField(max_length=310, null=True, blank=True)

    def __str__(self):
        return self.name or ''

class StateType(models.Model):
    name = models.CharField(max_length=310, null=True, blank=True)

    def __str__(self):
        return self.name or ''
