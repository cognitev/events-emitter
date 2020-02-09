from .models import BusinessRules, EventsDependencies
from django.contrib import admin


class BusinessRulesAdmin(admin.ModelAdmin):
    fields = ['event_type', 'state']


class EventsDependenciesAdmin(admin.ModelAdmin):
    fields = ['dependency_experssion']


admin.site.register(BusinessRules, BusinessRulesAdmin)
admin.site.register(EventsDependencies, EventsDependenciesAdmin)
