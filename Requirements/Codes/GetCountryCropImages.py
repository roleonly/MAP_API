from asyncore import read
from dbm import dumb
import json

from pickle import TRUE
from django.shortcuts import get_object_or_404
from matplotlib.patches import Polygon
import numpy
import rasterio
from rasterio.windows import Window
from matplotlib import pyplot
import os
from pathlib import Path
from rasterio.plot import show
import rasterio.mask
from django.core.serializers import serialize
from APIGEO.models import *
from django.http import  HttpResponse, JsonResponse
import rasterio
import rasterio.features
import rasterio.warp
from APIGEO.permissions import IsFromTurkey
from rest_framework.views import APIView



#need requests
#parcel_id   =4
#map_id      =1
#

BASE_DIR = Path(__file__).resolve().parent.parent



def crop_raster(parcel_id,map_id):
    obj=get_object_or_404(Map,id=parcel_id)
    src = rasterio.open(os.path.join(BASE_DIR,'rasters/'+map_id+'.tif'))
    
    
    asd=serialize('geojson',[obj],geometry_field='poly')
    asd=json.loads(asd)
    geoms=[asd['features'][0]['geometry']]
    

    #out_image, out_transform = rasterio.mask.mask(src, geoms, invert=True)
    out_image, out_transform = rasterio.mask.mask(src, geoms , crop=True)
    
   
    show(out_image, out_transform)
    return out_image, out_transform  

class Raster(APIView):
    permission_classes = (IsFromTurkey,)
    def get(self, request, format=None):
        parcel_id=request.query_params['parcel_id']
        map_id=request.query_params['map_id']
        src,transform=crop_raster(parcel_id,map_id) 
        


        datalist=[]
        datalist.append(str(src.max()))
        datalist.append(str(src.min()))
        datalist.append(str(src.mean()))
        print (datalist)

        data=json.dumps(datalist)


        return HttpResponse((data))