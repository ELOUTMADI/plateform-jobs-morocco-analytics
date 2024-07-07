from django import forms
from .models import Locations

class JobFilterForm(forms.Form):
    min_applicants = forms.IntegerField(label='Minimum Applicants', required=False)
    max_applicants = forms.IntegerField(label='Maximum Applicants', required=False)
    city = forms.ChoiceField(choices=[], required=False, label='City')

    def __init__(self, *args, **kwargs):
        super(JobFilterForm, self).__init__(*args, **kwargs)
        self.fields['city'].choices = [(city, city) for city in Locations.objects.values_list('city', flat=True).distinct()]
