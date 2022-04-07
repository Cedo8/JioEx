import geocoder
from geopy.geocoders import Nominatim


def current_latlng():
    gps = geocoder.ip('me')
    lat = gps.latlng[0]
    lng = gps.latlng[1]
    return lat, lng


def find_latlng(suburb):
    locator = Nominatim(user_agent="GetLocr")
    get_location = locator.geocoder(suburb)
    lat = get_location.latitude
    lng = get_location.logitude
    return lat, lng


def find_suburb(lat, lng):
    locator = Nominatim(user_agent="GetLoc")
    coordinates = f"{lat}, {lng}"
    location = locator.reverse(coordinates)
    address = location.raw["address"]
    suburb = address["suburb"]

    return suburb
