# admin.py
import openpyxl
from django.http import HttpResponse
from django.contrib import admin
from .models import ( 
ContratacionMain, processType, acroymsType, 
typologyType, resSecType, StateType,

ValueAdded, BpinProjectCode, ValueAffectedBpinProjCDP,
BudgetItems, ArticleName, ItemValue, Notification
)
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class ContratacionMainAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
        
admin.site.register(ContratacionMain, ContratacionMainAdmin)

admin.site.register(processType)
admin.site.register(acroymsType)
admin.site.register(typologyType)
admin.site.register(resSecType)
admin.site.register(StateType)


class ValueAddedAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
admin.site.register(ValueAdded, ValueAddedAdmin)


class BpinProjectCodeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
admin.site.register(BpinProjectCode, BpinProjectCodeAdmin)


class ValueAffectedBpinProjCDPAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
admin.site.register(ValueAffectedBpinProjCDP, ValueAffectedBpinProjCDPAdmin)


class BudgetItemsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
admin.site.register(BudgetItems, BudgetItemsAdmin)


class ArticleNameAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
admin.site.register(ArticleName, ArticleNameAdmin)


class ItemValueAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
admin.site.register(ItemValue, ItemValueAdmin)


class NotificationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
admin.site.register(Notification, NotificationAdmin)