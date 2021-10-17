#!./.venv/bin/python

# https://www.youtube.com/watch?v=Dz3rSZHnKkM

import sys, os

import phonenumbers
from phonenumbers import carrier
from phonenumbers import geocoder

from opencage.geocoder import OpenCageGeocode

import folium

mynumber = '+30'+sys.argv[1]

# find country
pepnumber = phonenumbers.parse(mynumber)
#print(carrier.name_for_number(pepnumber, "en"))
location = phonenumbers.geocoder.description_for_number(pepnumber, "en")
print(location)

# get lat and long from country
key = os.environ['OPENCAGEKEY']
geoc = OpenCageGeocode(key)
results = geoc.geocode(str(location))
lat = results[0]['geometry']['lat']
lng = results[0]['geometry']['lng']
print(lat, lng)

# make map from lat and long
myMap = folium.Map(location=[lat,lng], zoom_start=9)
folium.Marker([lat,lng], popup=location).add_to(myMap)
myMap.save("mylocation.html")
