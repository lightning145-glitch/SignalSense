import math
from geopy.geocoders import Nominatim

def geocode_address(address):
    """Convert a text address into lat/lon using free Nominatim service."""
    geo = Nominatim(user_agent="signalsense-demo")
    location = geo.geocode(address)
    if location:
        return location.latitude, location.longitude
    return None, None

def haversine(lat1, lon1, lat2, lon2):
    """Return distance in km between two lat/lon points."""
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)*2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)*2
    return 2 * R * math.asin(math.sqrt(a))