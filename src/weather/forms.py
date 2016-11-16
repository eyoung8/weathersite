from django import forms
from .utils import validate_location
from django.core.exceptions import ValidationError

class LocationForm(forms.Form):
    location = forms.CharField(
        label='',
         validators=[],
         widget = forms.TextInput(
                attrs = {
                "placeholder": "Enter location",
                }
            )
         )

    def clean_location(self):
        location = self.cleaned_data['location']
        if not isinstance(location, str):
            raise ValidationError("That's not a string! HOW'D YOU EVEN DO THIS?")

        location = validate_location(location)
        if (len(location.split()) > 2):
            raise ValidationError("Please enter in the form of city, (state/country) or a zip code")
        return location
