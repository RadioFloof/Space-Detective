import geocoder
from skyfield.api import utc
from datetime import datetime

def get_user_location():
    g = geocoder.ip('me')
    if g.ok:
        lat, lon = g.latlng
        address = g.city + ", " + g.country if g.city and g.country else "Unknown location"
        return lat, lon, address
    else:
        return None, None, None

def get_user_datetime():
    return datetime.now().replace(tzinfo=utc)
