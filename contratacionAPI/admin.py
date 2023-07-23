# admin.py
import openpyxl
from django.http import HttpResponse
from django.contrib import admin
from .models import ContratacionMain, processType, acroymsType, typologyType, resSecType, StateType
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class ContratacionMainAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
        
admin.site.register(ContratacionMain, ContratacionMainAdmin)

# admin.site.register(ContratacionMain)
admin.site.register(processType)
admin.site.register(acroymsType)
admin.site.register(typologyType)
admin.site.register(resSecType)
admin.site.register(StateType)