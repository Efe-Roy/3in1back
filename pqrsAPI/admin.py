from django.contrib import admin
from .models import PqrsMain, EntityType, NameType, MediumResType, StatusType, FileResNum, PqrsNotifify, PqrsFileNum
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class PqrsMainAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
        
admin.site.register(PqrsMain, PqrsMainAdmin)


admin.site.register(PqrsFileNum)
admin.site.register(FileResNum)
admin.site.register(EntityType)
admin.site.register(NameType)
admin.site.register(MediumResType)
admin.site.register(StatusType)
admin.site.register(PqrsNotifify)