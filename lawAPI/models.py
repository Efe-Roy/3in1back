from django.db import models
from Auth.models import User
from contratacionAPI.models import processType, resSecType

# Create your models here.
class PreviousStudyModel(models.Model):
    data_receive_mail = models.DateField()
    process = models.ForeignKey(processType, null=True, blank=True, on_delete=models.SET_NULL)
    responsible_secretary = models.ForeignKey(resSecType, null=True, blank=True, on_delete=models.SET_NULL)
    purpose_of_activities = models.TextField()
    worth = models.IntegerField()
    term = models.IntegerField()
    bpin_code = models.CharField(max_length=300, null=True, blank=True)
    lawyer_role = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={'is_lawyer': True})
    pdf = models.FileField(null=True, blank=True, upload_to='pdfs/lawyer/')
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.process} - {self.data_receive_mail}'


class OperationModel(models.Model):
    corporate_name = models.CharField(max_length=2300, null=True, blank=True)
    headquarter = models.CharField(max_length=2300, null=True, blank=True)
    area_of_operation = models.CharField(max_length=2300, null=True, blank=True)
    
    v_class = models.CharField(max_length=2300, null=True, blank=True)
    v_make = models.CharField(max_length=2300, null=True, blank=True)
    v_model = models.CharField(max_length=2300, null=True, blank=True)
    v_license_plate = models.CharField(max_length=2300, null=True, blank=True)
    v_cylinder_capacity = models.CharField(max_length=2300, null=True, blank=True)
    v_fuel_type = models.CharField(max_length=2300, null=True, blank=True)
    
    service_level = models.CharField(max_length=2300, null=True, blank=True)
    expiration_date = models.CharField(max_length=2300, null=True, blank=True)
    consecutive_numbering = models.CharField(max_length=2300, null=True, blank=True)
    
    authorize_signature = models.BooleanField(default=False)
    authorize_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    