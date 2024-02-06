from django.contrib import admin
from .models import SisbenMain, LocationType
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class SisbenMainAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
        
admin.site.register(SisbenMain, SisbenMainAdmin)

admin.site.register(LocationType)