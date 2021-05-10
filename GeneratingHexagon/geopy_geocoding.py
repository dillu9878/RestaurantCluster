import geopy
from geopy.geocoders import Nominatim


address = "D-228, Mohali"

geodata = Nominatim(user_agent='dillu').geocode(address)
print(geodata.latitude, geodata.longitude)
geodata = Nominatim(user_agent='dillu').reverse((geodata.latitude, geodata.longitude))
print(geodata)
