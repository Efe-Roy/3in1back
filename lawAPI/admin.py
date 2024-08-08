from django.contrib import admin
from .models import PreviousStudyModel, OperationModel

# Register your models here.
class OperationAdmin(admin.ModelAdmin):
    list_display = [
        'id', "corporate_name", "headquarter",
        "area_of_operation", "v_class",
        "v_make", "v_model", "v_license_plate",
        "v_cylinder_capacity", "v_fuel_type",
        "service_level", "expiration_date","consecutive_numbering"
    ]

admin.site.register(PreviousStudyModel);
admin.site.register(OperationModel, OperationAdmin);