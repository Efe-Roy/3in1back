from django.db import models

# Create your models here.
class LawFirmModel(models.Model):
    document = models.CharField(max_length=255)
    conservation = models.BooleanField(default=False)
    personal_services = models.BooleanField(default=False)
    work_contract = models.BooleanField(default=False)
    direct_contract = models.BooleanField(default=False)
    fulfills = models.CharField(max_length=255)
    
    def __str__(self):
        return self.document