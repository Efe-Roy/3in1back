from django.db import models

# Create your models here.

class SisbenMain(models.Model):
    citizenship_card = models.CharField(max_length=1000, null=True, blank=True)
    full_name = models.CharField(max_length=1000, null=True, blank=True)
    cell_phone = models.CharField(max_length=1000, null=True, blank=True)
    createdAt = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.full_name or ''
    