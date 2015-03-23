from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'EventFinder.views.home', name='home'),
    url(r'events', 'EventFinder.views.events', name='events')
)