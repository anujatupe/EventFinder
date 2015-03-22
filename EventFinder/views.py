from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.geoip import GeoIP
from django.shortcuts import render_to_response
from EventFinder.forms import CategoriesForm
import logging
import urllib2
import urllib
import json
from django.template import *

# Create your views here.
logger = logging.getLogger(__name__)

def home(request):
    if request.method == 'GET':
        g = GeoIP()
        geo_location = g.city('74.125.79.147')
        logger.debug("Geo location is...")
        logger.debug(geo_location)
        form = CategoriesForm()
    c = {}
    c.update({'form': form})
    return render_to_response("EventFinderProject/home.html", c)

@csrf_exempt
def events(request):
    logger.debug("REQUEST OBJECT IS ***********")
    logger.debug(request)
    form = CategoriesForm(request.GET)
    if form.is_valid():
        g = GeoIP()
        g.city(request.META['REMOTE_ADDR'])
        geo_location = g.city('74.125.79.147')
        request_params = urllib.urlencode({
                                            "token": "BJCBWSGK6STWD6FRC3UQ",
                                            "categories": ','.join(form.cleaned_data.get('category', [])),
                                            "location.latitude": geo_location['latitude'],
                                            "location.longitude": geo_location['longitude'],
                                            "location.within": "20mi",
                                            "sort_by": "date",
                                            "page": 1
                                        })
        events_url = "https://www.eventbriteapi.com/v3/events/search?"+request_params
        request = urllib2.Request(events_url)
        response = urllib2.urlopen(request)
        resp_parsed = json.loads(response.read())
        events_list = resp_parsed.get('events', None)
        next_events_url = urllib.urlencode({
            "page": 2,
            "user_categories": ','.join(form.cleaned_data.get('category', []))
        })
        return render_to_response("EventFinderProject/events.html", {"events_list": events_list, "previous_events_url": "", "next_events_url": "?"+next_events_url, "previous": "disabled", "next": ""})
    else:
        logger.debug("REQUEST OBJECT IS ***********")
        logger.debug(request)
        user_categories = request.GET.get('user_categories', '')
        page = int(request.GET.get('page', '0'))
        previous_enabled = "disabled" if (page <= 1) else ""
        previous_events_url = urllib.urlencode({
                                "page": str(page - 1),
                                "user_categories": user_categories
        }) if (page > 0) else ""
        next_events_url = urllib.urlencode({
            "page": str(page + 1),
            "user_categories": user_categories
        })
        g = GeoIP()
        g.city(request.META['REMOTE_ADDR'])
        geo_location = g.city('74.125.79.147')
        request_params = urllib.urlencode({
                                            "token": "BJCBWSGK6STWD6FRC3UQ",
                                            "categories": user_categories,
                                            "location.latitude": geo_location['latitude'],
                                            "location.longitude": geo_location['longitude'],
                                            "location.within": "20mi",
                                            "sort_by": "date",
                                            "page": page
                                        })
        events_url = "https://www.eventbriteapi.com/v3/events/search?"+request_params
        request = urllib2.Request(events_url)
        response = urllib2.urlopen(request)
        resp_parsed = json.loads(response.read())
        events_list = resp_parsed.get('events', None)
        # logger.debug("FIRST EVENT:")
        # logger.debug(events_list[0])
        return render_to_response("EventFinderProject/events.html", {"events_list" : events_list, "previous_events_url": "?"+previous_events_url, "next_events_url": "?"+next_events_url, "previous" : previous_enabled, "next" : "" })
    return render_to_response("EventFinderProject/events.html", "No name")


def _get_events():
    pass