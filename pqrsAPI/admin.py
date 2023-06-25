from django.contrib import admin
from .models import PqrsMain, EntityType, NameType, MediumResType, StatusType

# Register your models here.
admin.site.register(PqrsMain)
admin.site.register(EntityType)
admin.site.register(NameType)
admin.site.register(MediumResType)
admin.site.register(StatusType)