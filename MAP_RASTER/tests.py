from asyncio.windows_events import NULL
from inspect import Parameter
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from requests import delete

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


import rasterio
import rasterio.features
import rasterio.warp


import sqlalchemy
import rasterio
from rasterio.io import MemoryFile
from django.http import FileResponse
from xml.dom import minidom
from .models import Parcel


def read_from_xml(FilePath):
    mydoc=minidom.parse(FilePath)
    coords=mydoc.getElementsByTagName('GeoTransform')[0].firstChild.data
    my_list = coords.split(",")
    a=float(my_list[0])
    b=float(my_list[3])
    return [a,b]

    


    
def getraster(id):
    
    obj=Parcel.objects.get(id=id)
    
    
    
    geom=obj.poly
    url = sqlalchemy.engine.url.URL(drivername='postgresql+psycopg2',
                                    database='DB_API',
                                    username='gisadmin',
                                    password='Role1453',
                                    host='localhost',
                                    port=5432)
    engine = sqlalchemy.create_engine(url)
    
    
    sql = "SELECT ST_AsGDALRaster(ST_Union(rast), 'GTiff') AS tiff FROM worldmap as r WHERE ST_Intersects(ST_GeomFromText('"+str(geom)+"'),r.rast)"
    
    filename=str(id)
    with engine.connect() as cnxn:
        result = cnxn.execute(sql)
    
        data= result.fetchall() 
        tif_data = data[0][0]
        #tiff data write to file
        with open('static/'+filename+'.tif', 'wb') as f:
            f.write(tif_data)
        
        #tiff data read from file
        with rasterio.open('static/'+filename+'.tif') as src:
            data=src.read(1)
            data=np.ma.masked_where(data<-1500,data)
            print(data.shape[0],data.shape[1],data.max(),data.min(),data.metadata) 
        
    
    #    asd=MemoryFile(tif_data.tobytes())
    #    
    #    asdf=asd.open()
    #    
    #    data=asdf.read(1)
    ##delete values if they are not in the polygon
    #    
    #    
    #   
    #    
    #    #write data to file
    #    with rasterio.open('static/test.tif', 'w', driver='GTiff',    #GTiff
    #                         height=asdf.height, width=asdf.width, count=1,
    #                            dtype=asdf.dtypes[0] ,                  # asdf.dtypes[0],
    #                            crs={'init': 'epsg:4326'},
    #                            transform=asdf.transform) as dst:
    #        dst.write(data,1)
    #        print (dst.height,dst.width)
    #        
        
        
        #coords=read_from_xml('static/'+filename+'.png.aux.xml')
        #with Image.open('static/'+filename+'.png') as im:
        #    width,height=im.size
        #    
        #return JsonResponse( {'url':'http://localhost:8000/static/'+filename+'.png','coords':coords , 'imageW':width,'imageH':height } ,status=200)
        #send file to api endpoint
        
        
        #return HttpResponse(open('static/test.tif', 'rb'), content_type='image/png')
        
        
         
        
        
        
    #return test.tif file
    
    
        
        
        
        
    return ('OK')
        
        
getraster(5)       

            
        
        

# Create your tests here.
