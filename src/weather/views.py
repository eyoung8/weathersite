from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .weather import get_weather
from .forms import LocationForm
# Create your views here.

class WeatherView(View):
    def get(self, request, *args, **kwargs):
        form = LocationForm()
        context = {
            "title": 'Enter Location:',
            "form": form
        }
        return render(request, "weather/home.html", context)

    def post(self, request, *args, **kwargs):
        form = LocationForm(request.POST)
        template = "weather/home.html"
        context = {
            "form": form
        }
        if (form.is_valid()):
            location = form.cleaned_data.get("location")
            results = get_weather(location)
            if results:
                template = "weather/results.html"
                context['results'] =  results
            else:
                template = "weather/home.html"
                context["title"] = "That location couldn't be found"
        return render(request, template, context)