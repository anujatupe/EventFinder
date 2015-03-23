from django.test import TestCase
from EventFinder.forms import CategoriesForm

# Create your tests here.
class EventFinderTest(TestCase):
    def test_home(self):
      resp = self.client.get('/')
      self.assertTrue('form' in resp.context)
      self.assertEqual(resp.status_code, 200)

    def test_events(self):
      resp = self.client.get('/events')
      self.assertTrue('next_events_url' in resp.context)
      self.assertTrue('previous_events_url' in resp.context)
      self.assertTrue('events_list' in resp.context)
      self.assertTrue('previous' in resp.context)
      self.assertTrue('next' in resp.context)
      self.assertEqual(resp.status_code, 200)

    def test_valid_form(self):
		  data = {'category': ['103','109'] }
		  form = CategoriesForm(data=data)
		  self.assertTrue(form.is_valid())






