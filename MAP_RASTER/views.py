from asyncio.windows_events import NULL
from inspect import Parameter
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from requests import delete
from MAP_PARCEL.models import Parcel

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from drf_yasg.views import get_schema_view
from drf_yasg import openapi 
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.core.serializers import serialize

from django.shortcuts import get_object_or_404
from xml.dom import minidom
import numpy as np
import rasterio
from rasterio.windows import Window

import os
from pathlib import Path
from rasterio.plot import show
import rasterio.mask
from django.core.serializers import serialize

from django.http import  HttpResponse, JsonResponse
import rasterio
import rasterio.features
import rasterio.warp
#from pandas import DataFrame as df
#from PIL import Image
from rest_framework.views import APIView
import sqlalchemy
import rasterio
from rasterio.io import MemoryFile
from django.http import FileResponse
from xml.dom import minidom
from MAP_RASTER.serializer import RasterTiffSerializer
from MAP_RASTER.models import raster_tiff

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
            rast.URL='static/'+str(rid)+'.tif'
            rast.parcel=obj
            rast.raster_image=None
            rast.save()
            
            
            
    
    
    
    
    








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

        
        
       
                
        
        
            
            
        
            