"""events_emitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from tastypie.resources import ModelResource
from events_emitter.models import BusinessRules, EventsDependencies
from django.utils.translation import ugettext_lazy
from django.conf import settings
from django.conf.urls.static import static


class BusinessRulesResource(ModelResource):
    class Meta:
        queryset = BusinessRules.objects.all()
        resource_name = 'business_rule'


class EventsDependenciesResource(ModelResource):
    class Meta:
        queryset = EventsDependencies.objects.all()
        resource_name = 'events_dependency'


business_rule_resource = BusinessRulesResource()
event_dependency_resource = EventsDependenciesResource()


urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^api/', include(business_rule_resource.urls)),
    url(r'^api/', include(event_dependency_resource.urls)),
] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.PROMETHEUS_ENABLE_FLAG:
    urlpatterns += [url('', include('django_prometheus.urls'))]

admin.site.site_header = ugettext_lazy('Events Emitter Dashboard')
admin.site.index_title = ugettext_lazy('Business Events administration')
admin.site.site_header = ugettext_lazy('Events Emitter')
admin.site.site_title = ugettext_lazy('Events Emitter')
