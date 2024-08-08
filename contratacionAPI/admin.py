# admin.py
import openpyxl
from django.http import HttpResponse
from django.contrib import admin
from .models import ( 
ContratacionMain, processType, acroymsType, 
typologyType, resSecType, StateType, LawFirmModel,

ValueAdded, BpinProjectCode, ValueAffectedBpinProjCDP,
BudgetItems, ArticleName, ItemValue, Notification, BpinProjName
)
from import_export.admin import ImportExportModelAdmin

# Register your models here.
# class ContratacionMainAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#         ...
class ContratacionMainAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'process',
                    'process_num',
                    'acroyms_of_contract',
                    'typology',
                    'contact_no',
                    'real_executed_value_according_to_settlement',
                    'expense_type',
                    'contractor'
                    ]
#     list_display_links = [
#         'user',
#         'shipping_address',
#         'billing_address',
#         'payment',
#         'coupon'
#     ]
    list_filter = [
                   'responsible_secretary',
                   'acroyms_of_contract',
                   'typology']
    search_fields = [
        'real_executed_value_according_to_settlement',
        'contact_no',
        'process_num'
    ]


admin.site.register(ContratacionMain, ContratacionMainAdmin)

admin.site.register(LawFirmModel)
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


class BpinProjNameAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
admin.site.register(BpinProjName, BpinProjNameAdmin)


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