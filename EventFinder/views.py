from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.geoip import GeoIP
from django.shortcuts import render_to_response
from EventFinder.forms import CategoriesForm
import logging
import urllib2
import urllib
import json
from django.template import *

# Initialize the logger
logger = logging.getLogger(__name__)

def home(request):
  """Route for the landing page - choose the categories for the events to be searched

  Args:
      request: request object
  Returns:
      Sends categories to the events page for getting the events related to the categories
  """

  form = CategoriesForm()
  return render_to_response("EventFinderProject/home.html", {'form': form})

@csrf_exempt
def events(request):
  """Route for the events page - displays the events belonging to the category selected by the user

  Args:
      request: request object having get parameters. It has the category ids using which we search for events
  Returns:
      Renders a different page which has all the events related to the categories passed
  """

  g = GeoIP()
  ip_address = '74.125.79.147' if request.META['HTTP_X_FORWARDED_FOR'] == '127.0.0.1' else request.META['HTTP_X_FORWARDED_FOR']
  geo_location = g.city(ip_address)
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
    events_list, page_count = _get_events(request_params)
    previous_events_url, next_events_url = _get_next_previous_event_urls(1, ','.join(form.cleaned_data.get('category', [])), 50)
    next_enabled = "disabled" if page_count == 1 else ""
    return render_to_response("EventFinderProject/events.html", {"events_list": events_list, "previous_events_url": previous_events_url, "next_events_url": "?"+next_events_url, "previous": "disabled", "next": next_enabled})
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
    events_list, page_count = _get_events(request_params)
    next_enabled = "disabled" if page_count == page else ""
    return render_to_response("EventFinderProject/events.html", {"events_list" : events_list, "previous_events_url": "?"+previous_events_url, "next_events_url": "?"+next_events_url, "previous" : previous_enabled, "next" : next_enabled })


def _get_events(request_params):
  """Makes an API call to Eventbrite and gets all the events related to the categories that user wants

  Args:
      request_params: urlencoded dictionary of the get parameters to be sent to the API
  Returns:
      events_list: A list of dicts of the various events belonging to the category. Gets only the first 50 events.
      Paginated response from Eventbrite API.
      Also, returns the page count i.e. the total number of pages having the events.
  """

  events_url = "https://www.eventbriteapi.com/v3/events/search?"+request_params
  request = urllib2.Request(events_url)
  response = urllib2.urlopen(request)
  resp_parsed = json.loads(response.read())
  events_list = resp_parsed.get('events', None)
  return events_list, resp_parsed.get('pagination').get('page_count', 0)

def _get_next_previous_event_urls(page, user_categories, page_count):
  """Creates the URL to get previous page's events and the url to get the next page's events.

  Args:
      page: current page number
      user_categories: string of category ids selected by users. Category ids are separated by comma
      page_count: Total number of pages having the events
  Returns:
      previous_events_url: URL to get the events of previous page
      next_events_url: URL to get the events of next page
  """

  previous_events_url = urllib.urlencode({
                          "page": str(page - 1),
                          "user_categories": user_categories
  }) if (page > 1) else ""
  next_events_url = urllib.urlencode({
      "page": str(page + 1),
      "user_categories": user_categories
  }) if (page_count == 50) else ""

  return previous_events_url, next_events_url