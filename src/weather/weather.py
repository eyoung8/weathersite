
#/usr/bin/env python
"""Script that accesses and prints weather information on a city retrieved from yahoo's weather api. 
On command line specify city (lowercase, no spaces), state (lowercase, abbreviation, eg. ny) to select the location
Display options include: temp condition windchill high low humidity date location
Example call: python weather.py newyork ny temp condition windchill high low humidity date location"""

#API info:
#https://developer.yahoo.com/yql/console/#h=select+*+from+weather.forecast+where+woeid+in+(select+woeid+from+geo.places(1)+where+text%3D'dasdas%2C+asdafaf')
#https://developer.yahoo.com/weather/

import urllib.parse, urllib.request, json, sys

from .utils import is_zip

def get_temp(data):
    """Returns  temperature string"""
    return data['query']['results']['channel']['item']['condition']['temp']

def get_windchill_temp(data):
    """Returns feels like temperature string"""
    return data['query']['results']['channel']['wind']['chill']

def get_date(data):
    """Returns date/time of most recent weather update string"""
    return data['query']['results']['channel']['lastBuildDate']

def get_condition(data):
    """Returns weather condition string"""
    return data['query']['results']['channel']['item']['condition']['text']

def get_city(data):
    """Returns city string"""
    return data['query']['results']['channel']['location']['city']

def get_state(data):
    """Returns state (or region) string"""
    return data['query']['results']['channel']['location']['region']

def get_humidity(data):
    """Returns  humidity string"""
    return data['query']['results']['channel']['atmosphere']['humidity']

def get_sunrise(data):
    """Returns  sunrise string"""
    return data['query']['results']['channel']['astronomy']['sunrise']

def get_sunset(data):
    """Returns  sunset string"""
    return data['query']['results']['channel']['astronomy']['sunset']

def get_high(data):
    """Returns  high temperature string"""
    return data['query']['results']['channel']['item']['forecast'][0]['high']

def get_low(data):
    """Returns low temperature string"""
    return data['query']['results']['channel']['item']['forecast'][0]['low']

def get_location(data):
    """Returns formatted location as City, STATE"""
    return get_city(data) + ", " + get_state(data)

def get_yahoo_weather_json(query):
    """Returns a json file. Designed for accessing yahoo weather api."""
    base_url = "https://query.yahooapis.com/v1/public/yql?"
    format = "&format=json"
    final_url = base_url + urllib.parse.urlencode({'q':query}) + format
    req = urllib.request.urlopen(final_url).read().decode('utf-8')
    data = json.loads(req)
    return data

displayDict = { "temp" : ["Temperature: ", get_temp, " F"],
                "condition" : ["Condition: ", get_condition, ""],
                "date" : ["Accessed: ", get_date, ""],
                "windchill" : ["Feels like: ", get_windchill_temp, " F"],
                "high" : ["High: ", get_high, " F"],
                "low" : ["Low: ", get_low, " F"],
                "sunrise" : ["Sunrise: ", get_sunrise, ""],
                "sunset" : ["Sunset: ", get_sunset, ""],
                "humidity" : ["Humidity: ", get_humidity, "%"],
                "location" : ["", get_location, ""]
                }
displayDict["temp"]

def get_query(city, state):
    loc = city + ", " + state
    query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='"+ loc + "')"
    return query

def get_query_by_zip(loc):
    query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='"+ loc + "')"
    return query

def get_std_weather_results(data, settings=['location', 'temp', 'windchill', 'condition', 'high', 'low', 'humidity', 'date']):
    results = []
    for word in settings:
        try:
            results.append('{0}{1}{2}'.format(displayDict[word][0], displayDict[word][1](data), displayDict[word][2]))
        except KeyError as err:
            pass
    return results

def get_weather(location):
    query = None
    if (is_zip(location)):
        query = get_query_by_zip(location)
    else:
        city, state = location.split()
        query = get_query(city, state)
    data = get_yahoo_weather_json(query)
    results = get_std_weather_results(data)
    return results

def main():
    try:
        city = sys.argv[1]
        state = sys.argv[2]
        loc = city + ", " + state
        query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='"+ loc + "')"
        data = get_yahoo_weather_json(query)
        settings = sys.argv[3:]
        for word in settings:
            try:
                print('{0}{1}{2}'.format(displayDict[word][0], displayDict[word][1](data), displayDict[word][2]))
            except KeyError as err:
                print ("Not an option: {}".format(err))


    except IndexError as err:
        print ("Index Error: {}".format(err))

    except urllib.error.URLError:
        print("Weather Gods could not be reached",)
    

if __name__ == "__main__":
    main()