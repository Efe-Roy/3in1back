from django.contrib import admin
from .models import (
    PoliceCompliant, PoliceSubmissionLGGS, UrbanControl,
    TrafficViolationCompared, TrafficViolationComparedMyColission,
    ComplaintAndOfficeToAttend, File2Return2dOffice, InspNotifify
)
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class PoliceCompliantAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
admin.site.register(PoliceCompliant, PoliceCompliantAdmin)


admin.site.register(PoliceSubmissionLGGS)
admin.site.register(UrbanControl)
admin.site.register(TrafficViolationCompared)
admin.site.register(TrafficViolationComparedMyColission)
admin.site.register(ComplaintAndOfficeToAttend)
admin.site.register(File2Return2dOffice)
admin.site.register(InspNotifify)