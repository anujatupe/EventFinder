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
    form = CategoriesForm()
    return render_to_response("EventFinderProject/home.html", {'form': form})

@csrf_exempt
def events(request):
    g = GeoIP()
    g.city(request.META['REMOTE_ADDR'])
    geo_location = g.city('74.125.79.147')
    form = CategoriesForm(request.GET)
    request_params = {
                        "token": "BJCBWSGK6STWD6FRC3UQ",
                        "location.latitude": geo_location['latitude'],
                        "location.longitude": geo_location['longitude'],
                        "location.within": "20mi",
                        "sort_by": "date"
                    }
    if form.is_valid():
        request_params.update({
                                "categories": ','.join(form.cleaned_data.get('category', [])),
                                "page": 1
                            })
        request_params = urllib.urlencode(request_params)
        events_list = _get_events(request_params)
        previous_events_url, next_events_url = _get_next_previous_event_urls(1, ','.join(form.cleaned_data.get('category', [])), 50)
        return render_to_response("EventFinderProject/events.html", {"events_list": events_list, "previous_events_url": previous_events_url, "next_events_url": "?"+next_events_url, "previous": "disabled", "next": ""})
    else:
        user_categories = request.GET.get('user_categories', '')
        page = int(request.GET.get('page', '0'))
        previous_enabled = "disabled" if (page <= 1) else ""
        previous_events_url, next_events_url = _get_next_previous_event_urls(page, user_categories, 50)
        request_params.update({
                                "categories": user_categories,
                                "page": page
                            })
        request_params = urllib.urlencode(request_params)
        events_list = _get_events(request_params)
        return render_to_response("EventFinderProject/events.html", {"events_list" : events_list, "previous_events_url": "?"+previous_events_url, "next_events_url": "?"+next_events_url, "previous" : previous_enabled, "next" : "" })


def _get_events(request_params):
    events_url = "https://www.eventbriteapi.com/v3/events/search?"+request_params
    request = urllib2.Request(events_url)
    response = urllib2.urlopen(request)
    resp_parsed = json.loads(response.read())
    events_list = resp_parsed.get('events', None)
    return events_list

def _get_next_previous_event_urls(page, user_categories, page_count):
    previous_events_url = urllib.urlencode({
                            "page": str(page - 1),
                            "user_categories": user_categories
    }) if (page > 1) else ""
    next_events_url = urllib.urlencode({
        "page": str(page + 1),
        "user_categories": user_categories
    }) if (page_count == 50) else ""

    return previous_events_url, next_events_url