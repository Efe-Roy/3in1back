from django.contrib import admin
from .models import UserProfile, User, Agent, Team, Organisation, ActivityTracker, TicketUserAgent
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class UserProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
admin.site.register(UserProfile, UserProfileAdmin)


# class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#         ...

class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'username',
        'position',
        'is_team',
        'is_pqrs',
        'is_agent',
        'is_agent_org',
        'is_hiring',
        'is_hiring_org',
        'is_sisben',
        'is_consult',
        'is_ticket_admin',
        'is_ticket_agent',
        'is_lawyer'
    ]
    list_filter = ['is_team',
        'is_pqrs',
        'is_agent',
        'is_agent_org',
        'is_hiring',
        'is_hiring_org',
        'is_sisben',
        'is_consult',
        'is_ticket_admin',
        'is_ticket_agent',
        'is_lawyer']
    search_fields = ['username']

admin.site.register(User, UserAdmin)


class OrganisationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
admin.site.register(Organisation)


class AgentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
admin.site.register(Agent, AgentAdmin)


# class TeamAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#         ...
class TeamAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'organisation'
    ]
    search_fields = ['user']

admin.site.register(Team, TeamAdmin)


class ActivityTrackerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
admin.site.register(ActivityTracker, ActivityTrackerAdmin)


class TicketUserAgentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        ...
admin.site.register(TicketUserAgent, TicketUserAgentAdmin)