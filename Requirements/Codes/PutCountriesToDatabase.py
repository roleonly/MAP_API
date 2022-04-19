
import json

from django.contrib.gis.geos import fromstr

import django.contrib.gis.geos as gs

from MAP_PARCEL.models import Parcel

def delparcels():
    parcels=Parcel.objects.all()
    for i in parcels:
        i.delete()

def PutCountriesToDatabase():
    file=open('Requirements/files/countries.geojson')
    data=json.load(file)
    for i in data['features']:
       
        countryMap=Parcel()
        countryMap.name=i['properties']['ADMIN']
        countryMap.type=2
    
        if i['geometry']['type']=="MultiPolygon" :
            countryMap.poly=json.dumps(i['geometry'])
            
            
        else:   
            countryMap.poly=gs.MultiPolygon(   fromstr(json.dumps(i['geometry'])   ))
            
            
        countryMap.save()

def PutCitiesToDatabase():
    file=open('Requirements/files/turkey.json')
    data=json.load(file)
    for i in data['features']:
        
        city=Parcel()
        city.name=i['properties']['name']
        city.type=1
    
        if i['geometry']['type']=="MultiPolygon" :
            city.poly=json.dumps(i['geometry'])
            
            
        else:   
            city.poly=gs.MultiPolygon(   fromstr(json.dumps(i['geometry'])   ))
            
            
        #city.save()

