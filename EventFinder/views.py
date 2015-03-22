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
    if request.method == 'POST':
        logger.debug("REQUEST OBJECT IS ***********")
        logger.debug(request)
        form = CategoriesForm(request.POST)
        if form.is_valid():
            g = GeoIP()
            g.city(request.META['REMOTE_ADDR'])
            geo_location = g.city('74.125.79.147')
            request_params = urllib.urlencode({
                                                "token" : "BJCBWSGK6STWD6FRC3UQ",
                                                "categories" : ','.join(form.cleaned_data.get('category', [])),
                                                "location.latitude" : geo_location['latitude'],
                                                "location.longitude" : geo_location['longitude'],
                                                "location.within" : "20mi",
                                                "sort_by" : "date",
                                                "page" : 1
                                            })
            events_url = "https://www.eventbriteapi.com/v3/events/search?"+request_params
            request = urllib2.Request(events_url)
            response = urllib2.urlopen(request)
            resp_parsed = json.loads(response.read())
            events_list = resp_parsed.get('events', None)
            # logger.debug("FIRST EVENT:")
            # logger.debug(events_list[0])
            #   next_events_url = "?page=2&user_categories="+','.join(form.cleaned_data.get('category', []))
            next_events_url = urllib.urlencode({
                "page" : 2,
                "user_categories" : ','.join(form.cleaned_data.get('category', []))
            })
            return render_to_response("EventFinderProject/events.html", {"events_list" : events_list, "next_events_url" : "?"+next_events_url })
    elif request.method == 'GET':
        logger.debug("REQUEST OBJECT IS ***********")
        logger.debug(request)
        user_categories = request.GET.get('user_categories', '')
        page = int(request.GET.get('page', '0')) + 1
        #next_events_url = "?page="+str(page)+"&user_categories="+user_categories
        next_events_url = urllib.urlencode({
            "page" : str(page),
            "user_categories" : user_categories
        })
        g = GeoIP()
        g.city(request.META['REMOTE_ADDR'])
        geo_location = g.city('74.125.79.147')
        request_params = urllib.urlencode({
                                            "token" : "BJCBWSGK6STWD6FRC3UQ",
                                            "categories" : user_categories,
                                            "location.latitude" : geo_location['latitude'],
                                            "location.longitude" : geo_location['longitude'],
                                            "location.within" : "20mi",
                                            "sort_by" : "date",
                                            "page" : page
                                        })
        events_url = "https://www.eventbriteapi.com/v3/events/search?"+request_params
        request = urllib2.Request(events_url)
        response = urllib2.urlopen(request)
        resp_parsed = json.loads(response.read())
        events_list = resp_parsed.get('events', None)
        # logger.debug("FIRST EVENT:")
        # logger.debug(events_list[0])
        return render_to_response("EventFinderProject/events.html", {"events_list" : events_list, "next_events_url" : "?"+next_events_url })
    return render_to_response("EventFinderProject/events.html", "No name")


def _get_events():
    pass