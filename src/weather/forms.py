from django import forms
from .utils import validate_location
from django.core.exceptions import ValidationError

class LocationForm(forms.Form):
    location = forms.CharField(
        label='',
         validators=[],
         widget = forms.TextInput(
                attrs = {
                "placeholder": "Enter 'city, state' OR enter a zip code",
                }
            )
         )

    # def clean(self):
    #     cleaned_data = super(LocationForm, self).clean()
    #     location = cleaned_data.get('location')

    def clean_location(self):
        location = self.cleaned_data['location']
        if not isinstance(location, str):
            raise ValidationError

        location = validate_location(location)
        if (len(location.split()) > 2):
            raise ValidationError
        return location
