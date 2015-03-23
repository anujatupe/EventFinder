from django.test import TestCase
from EventFinder.forms import CategoriesForm
from EventFinder.helpers.events_helper import _update_urlencode_request_params, _get_previous_next_link_status, _get_next_previous_event_urls, _get_events
from EventFinderProject.settings import EVENTBRITE_API_KEY

class EventFinderTest(TestCase):

  # Testing Views starts here

  def test_home(self):
    """Testing the landing page - having the categories form
    """

    resp = self.client.get('/')
    self.assertTrue('form' in resp.context)
    self.assertEqual(resp.status_code, 200)

  def test_events(self):
    """Testing the events page - events shown after categories are selected
    """

    resp = self.client.get('/events?page=1&user_categories=113%2C105%2C104  ')
    self.assertTrue('next_events_url' in resp.context)
    self.assertTrue('previous_events_url' in resp.context)
    self.assertTrue('events_list' in resp.context)
    self.assertTrue('previous' in resp.context)
    self.assertTrue('next' in resp.context)
    self.assertEqual(resp.status_code, 200)

  # Testing Forms starts here

  def test_valid_form(self):
    """Testing the validity of the Categories form on the landing page.
       Also, tests API call to Eventbrite to get categories of events
    """

    data = {'category': ['103','109'] }
    form = CategoriesForm(data=data)
    self.assertTrue(form.is_valid())

  # Testing helper functions for events view

  def test_make_request_params(self):
    """Testing urlencoding of request params
    """

    expected_value = "token="+EVENTBRITE_API_KEY+"&location.longitude=-122.057403564&location.latitude=37.4192008972&location.within=20mi&page=1&categories=103%2C109&sort_by=date"
    request_params = {
      "token": EVENTBRITE_API_KEY,
      "location.latitude": "37.4192008972",
      "location.longitude": "-122.057403564",
      "location.within": "20mi",
      "sort_by": "date"
    }
    url_encoded_request_params = _update_urlencode_request_params("103,109", 1, request_params)
    self.assertEqual(expected_value, url_encoded_request_params)

  def test_get_events(self):
    """Testing API call to Eventbrite API for getting events belonging to categories given by user
    """

    request_params = {
      "token": EVENTBRITE_API_KEY,
      "location.latitude": "37.4192008972",
      "location.longitude": "-122.057403564",
      "location.within": "20mi",
      "sort_by": "date"
    }
    url_encoded_request_params = _update_urlencode_request_params("103,109", 1, request_params)
    events_list, page_count = _get_events(url_encoded_request_params)
    self.assertTrue(type(events_list) is list)
    self.assertTrue(type(page_count) is int)

  def test_previous_next_link_status(self):
    """Testing status of previous and next links based on the current page number and the number of pages provided by Eventbrite.
    """

    page_states = {
      1: {
          'expected_previous_status': "disabled",
          'expected_next_status': "",
      },
      2: {
          'expected_previous_status': "",
          'expected_next_status': "",
      },
      50: {
          'expected_previous_status': "",
          'expected_next_status': "disabled",
      }
    }

    for curr_page, value in page_states.iteritems():
      previous_link_status, next_link_status = _get_previous_next_link_status(50, curr_page)
      self.assertEqual(value['expected_previous_status'], previous_link_status)
      self.assertEqual(value['expected_next_status'], next_link_status)

  def test_get_next_previous_urls(self):
    """Testing URLs for previous and next links based on user categories, current page number, the number of pages provided by Eventbrite.
    """

    user_categories = "103,109"
    page_states = {
      1: {
          'expected_previous_link': "",
          'expected_next_link': "page=2&user_categories=103%2C109",
      },
      2: {
          'expected_previous_link': "page=1&user_categories=103%2C109",
          'expected_next_link': "page=3&user_categories=103%2C109",
      },
      50: {
          'expected_previous_link': "page=49&user_categories=103%2C109",
          'expected_next_link': "",
      }
    }
    for curr_page, value in page_states.iteritems():
      previous_url, next_url = _get_next_previous_event_urls(curr_page, user_categories, 50)
      self.assertEqual(value['expected_previous_link'], previous_url)
      self.assertEqual(value['expected_next_link'], next_url)


