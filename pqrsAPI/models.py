from django.db import models
from Auth.models import UserProfile, Agent, Team, User

# Create your models here.

class PqrsMain(models.Model):
    date_of_entry = models.DateTimeField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    entity_or_position = models.ForeignKey("EntityType", null=True, blank=True, on_delete=models.SET_NULL)
    subject = models.CharField(max_length=300, null=True, blank=True)
    file_num = models.CharField(max_length=300, null=True, blank=True)
    responsible_for_the_response = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.ForeignKey("NameType", null=True, blank=True, on_delete=models.SET_NULL)
    days_of_the_response = models.CharField(max_length=500, null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    status_of_the_response = models.ForeignKey("StatusType", null=True, blank=True, on_delete=models.SET_NULL)
    medium_of_the_response = models.ForeignKey("MediumResType", null=True, blank=True, on_delete=models.SET_NULL)
    date_of_response = models.DateTimeField(auto_now_add=True)
    file_res = models.CharField(max_length=300, null=True, blank=True)
    comment = models.CharField(max_length=300, null=True, blank=True)
    

class FileResNum(models.Model):
    name = models.CharField(max_length=310)

    def __str__(self):
        return self.name

class EntityType(models.Model):
    name = models.CharField(max_length=310)

    def __str__(self):
        return self.name

class NameType(models.Model):
    name = models.CharField(max_length=310)

    def __str__(self):
        return self.name

class StatusType(models.Model):
    name = models.CharField(max_length=310)

    def __str__(self):
        return self.name

class MediumResType(models.Model):
    name = models.CharField(max_length=310)

    def __str__(self):
        return self.name
    
