from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.geoip import GeoIP
from django.shortcuts import render_to_response
from EventFinder.forms import CategoriesForm
from EventFinder.helpers.events_helper import _get_events, _get_next_previous_event_urls, _get_previous_next_link_status, _update_urlencode_request_params
import logging
from EventFinderProject.settings import EVENTBRITE_API_KEY

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
  ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '74.125.79.147')
  geo_location = g.city(ip_address)
  form = CategoriesForm(request.GET)
  request_params = {
                      "token": EVENTBRITE_API_KEY,
                      "location.latitude": geo_location['latitude'],
                      "location.longitude": geo_location['longitude'],
                      "location.within": "20mi",
                      "sort_by": "date"
                  }
  if form.is_valid():
    categories_string = ','.join(form.cleaned_data.get('category', []))
    request_params = _update_urlencode_request_params(categories_string, 1, request_params)
    events_list, page_count = _get_events(request_params)
    previous_events_url, next_events_url = _get_next_previous_event_urls(1, categories_string, page_count)
    previous_enabled, next_enabled = _get_previous_next_link_status(page_count, 1)
    return render_to_response("EventFinderProject/events.html", {"events_list": events_list, "previous_events_url": previous_events_url, "next_events_url": "?"+next_events_url, "previous": previous_enabled, "next": next_enabled })
  else:
    user_categories = request.GET.get('user_categories', '')
    page = int(request.GET.get('page', '0'))
    request_params = _update_urlencode_request_params(user_categories, page, request_params)
    events_list, page_count = _get_events(request_params)
    previous_events_url, next_events_url = _get_next_previous_event_urls(page, user_categories, page_count)
    previous_enabled, next_enabled = _get_previous_next_link_status(page_count, page)
    return render_to_response("EventFinderProject/events.html", {"events_list" : events_list, "previous_events_url": "?"+previous_events_url, "next_events_url": "?"+next_events_url, "previous" : previous_enabled, "next" : next_enabled })


