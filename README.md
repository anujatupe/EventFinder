# EventFinder
EventFinder is a Django app to find the events belonging to the categories selected by the user. Supports Pagination.

Assumptions made -
1. Finding relevant elevants meaning finding events around - Assumed near to be "20 miles". Uses GeoIP to find user's location.
2. Asked user for top 3 categories - Assumed user cannot select more than 3 categories


Unit Tests -
Run tests using command: python manage.py test EventFinder

Installation -
1) Install Django
2) Install MaxMind GeoIP C API


