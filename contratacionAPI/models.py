from django.db import models
# from Auth.models import User

# Create your models here.
class ServiceSegment(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name or ''
    
class ValueAdded(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name or ''

class BpinProjectCode(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name or ''
    
class BpinProjName(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name or ''

class ValueAffectedBpinProjCDP(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name or ''
    
class SourceOfResources(models.Model):
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
    
class ContratacionManager(models.Manager):
    def get_queryset(self):
        # return super().get_queryset() #all data
        return super().get_queryset().filter(is_deleted=False)
    
class ContratacionMain(models.Model):
    is_active = models.BooleanField(default=False)
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
    program = models.CharField(max_length=2300, null=True, blank=True)
    duration = models.CharField(max_length=2300, null=True, blank=True)
    contract_date = models.DateField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    finish_date = models.DateField(null=True, blank=True)
    advance = models.CharField(max_length=2310, null=True, blank=True)
    report_secop_begins = models.DateField(null=True, blank=True)
    secop_contract_report = models.DateField(null=True, blank=True)
    # report_honest_antioquia = models.DateField(null=True, blank=True)
    report_institute_web = models.DateField(null=True, blank=True)
    sia_observe_report = models.DateField(null=True, blank=True) #transparent_management_report
    act_liquidation = models.DateField(null=True, blank=True)
    settlement_report = models.DateField(null=True, blank=True)
    close_record = models.DateField(null=True, blank=True)
    report_date = models.DateField(null=True, blank=True)
    addition = models.CharField(max_length=2310, null=True, blank=True)
    url_1 = models.CharField(max_length=2310, null=True, blank=True)
    url_2 = models.CharField(max_length=2310, null=True, blank=True)
    extra_time = models.CharField(max_length=2310, null=True, blank=True)
    expense_type = models.CharField(max_length=2310, null=True, blank=True)
    # bpin_proj_name = models.CharField(max_length=2310, null=True, blank=True)

    value_added = models.ManyToManyField(ValueAdded)
    service_segment = models.ManyToManyField(ServiceSegment)
    bpin_project_code = models.ManyToManyField(BpinProjectCode)
    bpin_proj_name = models.ManyToManyField(BpinProjName)
    value_affected_bpin_proj_cdp = models.ManyToManyField(ValueAffectedBpinProjCDP)
    source_of_resources = models.ManyToManyField(SourceOfResources)
    budget_items = models.ManyToManyField(BudgetItems)
    article_name = models.ManyToManyField(ArticleName)
    item_value = models.ManyToManyField(ItemValue)

    state = models.ForeignKey("StateType", null=True, blank=True, on_delete=models.SET_NULL)
    responsible_secretary = models.ForeignKey("resSecType", null=True, blank=True, on_delete=models.SET_NULL)
    name_supervisor_or_controller = models.CharField(max_length=2310, null=True, blank=True)
    observations = models.CharField(max_length=2310, null=True, blank=True)
    contract_value_plus = models.CharField(max_length=2310, null=True, blank=True)
    real_executed_value_according_to_settlement = models.CharField(max_length=2310, null=True, blank=True)
    file_status = models.CharField(max_length=2310, null=True, blank=True)

    # purpose of track and trace of soft delete
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    objects = ContratacionManager()

    def __str__(self):
        return str(self.contact_no) or ''
    
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



class Notification(models.Model):
    msg = models.CharField(max_length=1000)
    createdAt = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.msg or ''
    

class LawFirmModel(models.Model):
    contract = models.ForeignKey("ContratacionMain", related_name="contratacion", on_delete=models.CASCADE, null=True, blank=True)
    document = models.TextField()
    conservation = models.CharField(max_length=255)
    # conservation = models.BooleanField(default=False)
    personal_services = models.BooleanField(default=False)
    work_contract = models.BooleanField(default=False)
    direct_contract = models.BooleanField(default=False)
    fulfills = models.CharField(max_length=255)
    
    def __str__(self):
        return self.document
    