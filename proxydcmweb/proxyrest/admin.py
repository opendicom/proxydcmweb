from django.contrib import admin
from proxyrest import models


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'aet', 'url']

admin.site.register(models.Institution, InstitutionAdmin)


class StaticParameterAdmin(admin.ModelAdmin):
    list_display = ['user', 'institution', 'parameter', 'active']

admin.site.register(models.StaticParameter, StaticParameterAdmin)


class SessionRestAdmin(admin.ModelAdmin):
    list_display = ['sessionid', 'start_date', 'expiration_date', 'user']

admin.site.register(models.SessionRest, SessionRestAdmin)
