from django.db import models

# Create your models here.
class PoliceSubmissionLGGS(models.Model):
    name = models.CharField(max_length=2300, null=True)
    Id_card = models.CharField(max_length=2300, null=True)
    appearance_num = models.CharField(max_length=2300, null=True)
    act_num = models.CharField(max_length=2300, null=True)

class UrbanControl(models.Model):
    filed = models.CharField(max_length=2300, null=True)
    date_received = models.DateTimeField()
    Involved_applicant = models.CharField(max_length=2300, null=True)
    res_report = models.CharField(max_length=2300, null=True)

class PoliceCompliant(models.Model):
    filed = models.CharField(max_length=2300, null=True)
    date_received = models.DateTimeField()
    complainants = models.CharField(max_length=2300, null=True)
    defendants = models.CharField(max_length=2300, null=True)

class TrafficViolationCompared(models.Model):
    date_events = models.DateTimeField()
    date_received = models.DateTimeField()
    involved = models.CharField(max_length=2300, null=True)
    id_card = models.CharField(max_length=2300, null=True)
    violation_code = models.CharField(max_length=2300, null=True)
    res_procedure = models.CharField(max_length=2300, null=True)

class TrafficViolationComparedMyColission(models.Model):
    date_received = models.DateTimeField()
    involved = models.CharField(max_length=2300, null=True)
    res_procedure = models.CharField(max_length=2300, null=True)

class ComplaintAndOfficeToAttend(models.Model):
    filed = models.CharField(max_length=2300, null=True)
    date_received = models.DateTimeField()
    affair = models.CharField(max_length=2300, null=True)

class File2Return2dOffice(models.Model):
    filed = models.CharField(max_length=2300, null=True)
    guy = models.DateTimeField()
    involved = models.CharField(max_length=2300, null=True)