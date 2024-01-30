from django.db import models

# Create your models here.

class SisbenMain(models.Model):
    citizenship_card = models.CharField(max_length=100, unique=True, null=True, blank=True)
    # citizenship_card = models.CharField(max_length=100, null=True, blank=True)
    full_name = models.CharField(max_length=150, null=True, blank=True)
    cell_phone = models.CharField(max_length=20, null=True, blank=True)
    location = models.ForeignKey("LocationType", null=True, blank=True, on_delete=models.SET_NULL)
    email = models.EmailField(null=True, blank=True)
    doc_type = models.CharField(max_length=250, null=True, blank=True)
    sex = models.CharField(max_length=150, null=True, blank=True)
    createdAt = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.full_name or ''
    

class LocationType(models.Model):
    name = models.CharField(max_length=310)

    def __str__(self):
        return self.name