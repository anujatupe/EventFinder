# EventFinder
EventFinder is a Django app to find the events belonging to the categories selected by the user. Supports Pagination.<br>

<b>Assumptions made - </b> <br>
1. Finding relevant elevants meaning finding events around - Assumed near to be "20 miles". Uses GeoIP to find user's location. <br>
2. Asked user for top 3 categories - Assumed user cannot select more than 3 categories<br>


<b>Unit Tests - </b> <br>
Run tests using command: python manage.py test EventFinder <br>

<b>Installation - </b> <br>
1) Install Django <br>
2) Install MaxMind GeoIP C API <br>


