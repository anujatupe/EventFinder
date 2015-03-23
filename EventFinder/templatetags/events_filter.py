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

@register.filter(name='event_image_filter')
def event_image_filter(image_src):
  """ Returns the path to a default image if events image is not given by Eventbrite API call

    Args:
      image_src: URL to the image of the event. Given by the API call to Eventbrite
    Returns:
      Returns a valid image src. Valid mmeaning it checks if the URL is empty.
      If URL is empty, returns path to default image, else the URL to events image.
  """
  return image_src if image_src != "" else "/static/images/default_events.png"

@register.filter(name='city_filter')
def city_filter(city, region):
  """Returns valid city string if None is present for city.

    Args:
      city: City where the event will be held. Given by the API call to Eventbrite.
      region: Region where the event will be held. Given by the API call to Eventbrite.
    Returns:
      If value of city and region is not equal to None, returns city with a comma appended
      If value of city is not None but region is None, returns city
      If value of city and region is None, returns empty string
  """

  if city != None and region != None:
    return city+', '
  elif city != None:
    return city
  else:
    return ""

@register.filter(name='region_filter')
def region_filter(region):
  """Returns valid region string if None is present for region.

    Args:
      region: Region where the event will be held. Given by the API call to Eventbrite.
    Returns:
      If value of region is not None, returns region
      If value of region is None, returns empty string
  """

  return region if region != None else ""

@register.filter(name='desc_filter')
def desc_filter(desc):
  """Returns valid description string if None is present for description.

    Args:
      desc: Description of the event which will be held. Given by the API call to Eventbrite.
    Returns:
      If value of desc is not None, returns description
      If value of desc is None, returns empty string
  """

  return desc if desc != None else ""
