from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'EventFinderProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)
    url(r'^$', 'EventFinder.views.home', name='home'),
    url(r'events', 'EventFinder.views.events', name='events')
) #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)