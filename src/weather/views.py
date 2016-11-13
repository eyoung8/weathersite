from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .weather import get_weather
from .forms import LocationForm
# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        form = LocationForm()
        context = {
            "title": 'Enter Location:',
            "form": form
        }
        return render(request, "weather/home.html", context)

    def post(self, request, *args, **kwargs):
        form = LocationForm(request.POST)
        context = {
            "title": 'Enter Location:',
            "form": form
        }
        template = "weather/home.html"
        if (form.is_valid()):
            location = form.cleaned_data.get("location")
            context['results'] = get_weather(location)
            template = "weather/results.html"
            print(context)

        return render(request, template, context)