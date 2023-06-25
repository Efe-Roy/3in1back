from django.contrib import admin
from .models import ContratacionMain, processType, acroymsType, typologyType, resSecType, StateType

# Register your models here.
admin.site.register(ContratacionMain)
admin.site.register(processType)
admin.site.register(acroymsType)
admin.site.register(typologyType)
admin.site.register(resSecType)
admin.site.register(StateType)