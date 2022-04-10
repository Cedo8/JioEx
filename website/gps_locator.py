import geocoder
from geopy.geocoders import Nominatim
import geopy.distance


def current_latlng():
    gps = geocoder.ip('me')
    lat = gps.latlng[0]
    lng = gps.latlng[1]
    return lat, lng


def find_latlng(suburb):
    locator = Nominatim(user_agent="GetLocr")
    get_location = locator.geocode(suburb)
    lat = get_location.latitude
    lng = get_location.longitude
    return lat, lng


def distance(loc1, loc2):
    return geopy.distance.geodesic(loc1, loc2).m
