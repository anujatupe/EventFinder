from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='events_date_filter')
def events_date_filter(value):
  """Filter for changing the date format to a human readable format

    Args:
        value: Time in unicode format
    Returns:
        Time in a human readable format
    """

  time_obj = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
  return time_obj