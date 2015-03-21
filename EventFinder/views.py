#from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.geoip import GeoIP
from django.shortcuts import render
from django.shortcuts import render_to_response
#from EventFinder.forms import NameForm
from EventFinder.forms import CategoriesForm
from django.views.generic.edit import FormView
import logging
import urllib2
import urllib
import json

# Create your views here.
logger = logging.getLogger(__name__)

# class ContactView(FormView):
#     template_name = 'home.html'
#     form_class = ContactForm
#     success_url = '/thanks/'
#
#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         form.send_email()
#         return super(ContactView, self).form_valid(form)


# def home(request):
#     APP_TOKEN = urllib.urlencode({"token" : "BJCBWSGK6STWD6FRC3UQ"})
#     categories_url = "https://www.eventbriteapi.com/v3/categories/?"+APP_TOKEN
#     request = urllib2.Request(categories_url)
#     response = urllib2.urlopen(request)
#     resp_parsed = json.loads(response.read())
#     #logger.debug(resp_parsed)
#     categories = resp_parsed['categories']
#     # for each in categories:
#     #     logger.debug(each['id'])
#     #     logger.debug(each['name'])
#     return render_to_response("EventFinderProject/home.html", { 'categories' : resp_parsed['categories'] })



# def home(request):
#     if request.method == 'GET':
#         form = NameForm()
#     c = {}
#     c.update({'form': form})
#     return render_to_response("EventFinderProject/home.html", c)
#
#
# @csrf_exempt
# def events(request):
#     form = NameForm(request.POST)
#     if form.is_valid():
#         logger.debug("The content is:")
#         logger.debug(form.cleaned_data)
#         return render_to_response("EventFinderProject/events.html", form.cleaned_data)
#     return render_to_response("EventFinderProject/events.html", "No name")

def home(request):
    if request.method == 'GET':
        g = GeoIP()
        geo_location = g.city('74.125.79.147')
        logger.debug("Geo location is...")
        logger.debug(geo_location)
        form = CategoriesForm()
    c = {}
    c.update({'form': form})
    logger.debug("FORM IS :")
    logger.debug(form)
    return render_to_response("EventFinderProject/home.html", c)


@csrf_exempt
def events(request):
    form = CategoriesForm(request.POST)
    if form.is_valid():
        g = GeoIP()
        g.city(request.META['REMOTE_ADDR'])
        geo_location = g.city('74.125.79.147')
        logger.debug("The content is:")
        logger.debug(form.cleaned_data)
        REQUEST_PARAMS = urllib.urlencode({
                                            "token" : "BJCBWSGK6STWD6FRC3UQ",
                                            "categories" : "103,109",
                                            #"venue.country" : geo_location['country_name'],
                                            #"venue.region" : geo_location['region'],
                                            #"venue.city" : geo_location['city']
                                            "location.latitude" : geo_location['latitude'],
                                            "location.longitude" : geo_location['longitude'],
                                            "location.within" : "4mi",
                                            "sort_by" : "date"
                                        })
        events_url = "https://www.eventbriteapi.com/v3/events/search?"+REQUEST_PARAMS
        request = urllib2.Request(events_url)
        response = urllib2.urlopen(request)
        resp_parsed = json.loads(response.read())
        events_list = resp_parsed.get('events', None)
        #event_names = [each['name']['text'] for each in events_list]
        #logger.debug("****Events nearby are*****")
        #logger.debug(event_names)
        return render_to_response("EventFinderProject/events.html", {"events_list" : events_list })
    return render_to_response("EventFinderProject/events.html", "No name")