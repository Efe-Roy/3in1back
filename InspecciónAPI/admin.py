from django.contrib import admin
from .models import (
    PoliceCompliant, PoliceSubmissionLGGS, UrbanControl,
    TrafficViolationCompared, TrafficViolationComparedMyColission,
    ComplaintAndOfficeToAttend, File2Return2dOffice
)

# Register your models here.
admin.site.register(PoliceCompliant)
admin.site.register(PoliceSubmissionLGGS)
admin.site.register(UrbanControl)
admin.site.register(TrafficViolationCompared)
admin.site.register(TrafficViolationComparedMyColission)
admin.site.register(ComplaintAndOfficeToAttend)
admin.site.register(File2Return2dOffice)