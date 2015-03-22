from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='events_date_filter')
def events_date_filter(value):
  time_obj = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
  return time_obj