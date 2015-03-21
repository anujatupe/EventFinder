from django import forms
import urllib
import urllib2
import json

class NameForm(forms.Form):
    # APP_TOKEN = urllib.urlencode({"token" : "BJCBWSGK6STWD6FRC3UQ"})
    # categories_url = "https://www.eventbriteapi.com/v3/categories/?"+APP_TOKEN
    # request = urllib2.Request(categories_url)
    # response = urllib2.urlopen(request)
    # resp_parsed = json.loads(response.read())
    # CATEGORY_CHOICES = ()
    # category = forms.MultipleChoiceField(required=True,
    #     widget=forms.CheckboxSelectMultiple, choices=CATEGORY_CHOICES)
    name = forms.CharField()

class CategoriesForm(forms.Form):
    APP_TOKEN = urllib.urlencode({"token" : "BJCBWSGK6STWD6FRC3UQ"})
    categories_url = "https://www.eventbriteapi.com/v3/categories/?"+APP_TOKEN
    request = urllib2.Request(categories_url)
    response = urllib2.urlopen(request)
    resp_parsed = json.loads(response.read())
    categories = resp_parsed.get('categories', None)
    if(categories):
        categories_list = [(each['id'], each['name']) for each in categories]
        CATEGORY_CHOICES = tuple(categories_list)

    category = forms.MultipleChoiceField(required=True,
         widget=forms.CheckboxSelectMultiple, choices=CATEGORY_CHOICES)

