from django.contrib import admin
from .models import UserProfile, User, Agent, Team, Organisation
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class UserProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
admin.site.register(UserProfile, UserProfileAdmin)


class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
admin.site.register(User, UserAdmin)


class OrganisationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
admin.site.register(Organisation)


class AgentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
admin.site.register(Agent, AgentAdmin)


class TeamAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
admin.site.register(Team, TeamAdmin)