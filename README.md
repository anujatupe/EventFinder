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

<b>Settings File</b> <br>
1. settings.local and wsgi.local - If you need to install the app locally, you need to copy the contents of these files to settings.py and wsgi.py respectively <br>
2. settings.prod and wsgi.prod - If you need to deploy this app, you need to copy the contents of these files to settings.py and wsgi.py respectively and then start the deploy



