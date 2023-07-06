from django.contrib import admin
from .models import UserProfile, User, Agent, Team, Organisation


# @admin.register(UserProfile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['user', 'date_of_birth', 'image']


admin.site.register(UserProfile)
admin.site.register(User)
admin.site.register(Organisation)
admin.site.register(Agent)
admin.site.register(Team)