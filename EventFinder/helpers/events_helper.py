import urllib2
import urllib
import json

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
  }) if (page < page_count) else ""

  return previous_events_url, next_events_url

def _get_previous_next_link_status(page_count, page):
  """Returns the status of the previous and next link on the events page.

  Args:
    page: current page number
    page_count: Total number of pages having the events
  Returns:
    previous_enabled: status of the previous link - "disabled" or ""
    next_enabled: status of the next link - "disabled" or ""
  """

  previous_enabled = "disabled" if (page <= 1) else ""
  next_enabled = "disabled" if page_count == page else ""
  return previous_enabled, next_enabled

def _update_urlencode_request_params(categories, page, request_params):
  """Updates the request params dict with categories and current page number and urlencodes the request params

  Args:
    categories: string of categories ids selected by the user
    page: current page number
    request_params: Request params to be sent to the Eventbrite API
  Returns:
    updated urlencoded request params
  """

  request_params.update({
                          "categories": categories,
                          "page": page
                      })
  return urllib.urlencode(request_params)