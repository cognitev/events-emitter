from events_emitter.models import BusinessRules, EventsDependencies
from django.contrib import admin
from events_emitter.signals import *# noqa


class BusinessRulesAdmin(admin.ModelAdmin):
    fields = ['event_type', 'state', 'duration']


class EventsDependenciesAdmin(admin.ModelAdmin):
    fields = ['dependency_experssion', 'event_name']


admin.site.register(BusinessRules, BusinessRulesAdmin)
admin.site.register(EventsDependencies, EventsDependenciesAdmin)
