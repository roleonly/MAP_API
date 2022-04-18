from asyncio.windows_events import NULL

import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from requests import delete
from MAP_PARCEL.models import Parcel

from rest_framework.views import APIView

from django.contrib.auth.models import User



from rest_framework.permissions import AllowAny, IsAuthenticated


from _Functions.geotiff_dem_colorization import GeoTIFF_to_color_dem
from django.shortcuts import get_object_or_404
from xml.dom import minidom
import numpy as np
import rasterio
from rasterio.windows import Window
import random
import string
import os
from pathlib import Path
from rasterio.plot import show
import rasterio.mask
from django.core.serializers import serialize

from django.http import  HttpResponse, JsonResponse
import rasterio
import rasterio.features
import rasterio.warp

from rest_framework.views import APIView
import sqlalchemy
import rasterio

from xml.dom import minidom
from MAP_RASTER.serializer import RasterTiffSerializer,RasterPNGSerializer
from MAP_RASTER.models import raster_tiff,raster_image

def createRasterTiff(rid:int):
    obj=Parcel.objects.get(id=rid)
    geom=obj.poly
    url = sqlalchemy.engine.url.URL(drivername='postgresql+psycopg2',
                                        database='DB_API',
                                        username='gisadmin',
                                        password='Role1453',
                                        host='localhost',
                                        port=5432)
    engine = sqlalchemy.create_engine(url)
        
        
    sql = "SELECT ST_AsGDALRaster(ST_Union(rast), 'GTiff') AS tiff FROM worldmap as r WHERE ST_Intersects(ST_GeomFromText('"+str(geom)+"'),r.rast)"
    

    with engine.connect() as cnxn:
        result = cnxn.execute(sql)
    
        data= result.fetchall() 
        tif_data = data[0][0]
       
        #tiff data write to file
        with open('static/'+str(rid)+'.tif', 'wb') as f:
            f.write(tif_data)
        
        #tiff data read from file
        with rasterio.open('static/'+str(rid)+'.tif') as src:
            data=src.read(1)
            data=np.ma.masked_where(data<-1500,data)

            rast=raster_tiff()
            
            rast.latitude=src.meta['transform'][5]   
            rast.longitude=src.meta['transform'][2]
            rast.width=src.meta['width']
            rast.height=src.meta['height']
            rast.elevation_max=data.max()
            rast.elevation_min=data.min()
            rast.scale=src.meta['transform'][0]
            rast.URL='http://127.0.0.1:8000/static/'+str(rid)+'.tif'
            rast.parcel=obj
            rast.raster_image=None
            rast.save()
            
            
            
    
    
    
    
    


def get_random_String(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str





class GetRasterImage(APIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, format=None):
        objID=request.GET.get('rid')
        # if an object with the id exists, return the URL of the raster image
        if raster_tiff.objects.filter(parcel_id=objID).exists():
            rast=raster_tiff.objects.get(parcel_id=objID)
            
            serialized=RasterTiffSerializer(rast)
            
            return JsonResponse(serialized.data, safe=False)
        else:
            # if the object does not exist, create it and return the URL of the raster image
            createRasterTiff(objID)
            rast=raster_tiff.objects.get(parcel_id=objID)
            
            serialized=RasterTiffSerializer(rast)
            return JsonResponse(serialized.data, safe=False)

class GetColoredImages(APIView)  :      
    permission_classes = (IsAuthenticated, )
    def get(self, request, format=None):
        objID=request.GET.get('rid')
        
        while True:

            try:
                rast=raster_tiff.objects.get(parcel_id=objID)
                break
            except:
                continue

        user=request.user
        PNG=raster_image.objects.filter(raster_id=rast.id,user=user)
        if PNG.exists():
            serialized=RasterPNGSerializer(PNG,many=True)
            return JsonResponse(serialized.data, safe=False)
        else:
            return JsonResponse({}, safe=False)
    
    def post(self, request, format=None):
        objID=request.GET.get('rid')
        
        rast=raster_tiff.objects.get(parcel_id=objID)
            
        
        outputPath='static/'+get_random_String(16)+'.png'
        GeoTIFF_to_color_dem(rast.URL, outputPath).colorize_dem()
        tif=raster_image( )
        tif.URL='http://127.0.0.1:8000/'+outputPath
        tif.xmlURL=tif.URL+'.aux.xml'
        tif.raster=rast
        tif.user=request.user
        tif.save()
        serialized=RasterPNGSerializer(tif)
        return JsonResponse(serialized.data, safe=False)

    def delete(self, request, format=None):
        objID=request.GET.get('rid')
        print(objID)
        
        PNG=raster_image.objects.filter(id=objID)
        PNG.delete()
        return JsonResponse({}, safe=False)

       
                
        
        
            
            
        
            