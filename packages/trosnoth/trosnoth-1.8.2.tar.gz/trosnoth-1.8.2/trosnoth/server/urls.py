from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^', include('trosnoth.djangoapp.urls', namespace='trosnoth')),
    url(r'^admin/', include(admin.site.urls)),
)
