from urllib2 import urlopen
from urllib import quote_plus
from urlparse import urlparse
from json import loads

from django import forms as forms

from models import Story

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('created', 'approved', 'lat', 'lng',)

    def clean_location(self):
        '''
        Use Google's Geocoding API to verify the given location.
        If it exists, set the lat/lng attributes.
        '''
        location = self.cleaned_data['location']
        gc_url = ("https://maps.googleapis.com/maps/api/geocode/json?"
                "address=%s"
                "&sensor=false"
                % (quote_plus(location)))
        gc_dict = loads(urlopen(gc_url).read())

        # status returns OK or ZERO_RESULTS
        if gc_dict['status'] == 'OK':
            self.cleaned_data['lat'] = float(
                    gc_dict['results'][0]['geometry']['location']['lat'])
            self.cleaned_data['lng'] = float(
                    gc_dict['results'][0]['geometry']['location']['lng'])
        else:
            raise forms.ValidationError("We couldn't resolve this location.")

        return location
