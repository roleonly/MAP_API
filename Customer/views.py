from inspect import Parameter
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from requests import delete
from Customer.models import Customer,CustomerParcel,Parcel
from Customer.Serializer import CustomerParcelSerializer,AuthSerializer
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

import numpy as np
import rasterio
from rasterio.windows import Window
from matplotlib import pyplot
import os
from pathlib import Path
from rasterio.plot import show
import rasterio.mask
from django.core.serializers import serialize

from django.http import  HttpResponse, JsonResponse
import rasterio
import rasterio.features
import rasterio.warp
from pandas import DataFrame as df

from rest_framework.views import APIView
import sqlalchemy
import rasterio
from rasterio.io import MemoryFile
from django.http import FileResponse

class Auth(APIView):
    #serializer_class = AuthSerializer    
    permission_classes = (AllowAny,)
    @swagger_auto_schema( request_body=AuthSerializer)

    def post(self,request):
        serializer=AuthSerializer(data=request.data)
        if serializer.is_valid():
            
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)

class CParcel(APIView):


    
    
    permission_classes = (IsAuthenticated,)
    

    def get(self,request):
        customer=Customer.objects.get(user=request.user)
        parcels=CustomerParcel.objects.filter(owner=customer)
        serializer=CustomerParcelSerializer(parcels,many=True)
        return JsonResponse(serializer.data,safe=False)
    
    @swagger_auto_schema( request_body=CustomerParcelSerializer)
    def post(self,request):
        serializer=CustomerParcelSerializer(data=request.data)
        if serializer.is_valid():
            
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)
    
    def delete(self,request,pk):
        customer=Customer.objects.get(user=request.user)
        parcels=CustomerParcel.objects.filter(owner=customer)
        parcel=parcels.get(id=pk)
        parcel.delete()
        return JsonResponse({'message':'deleted'},status=200)


class City(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, format=None):
        City=request.query_params['Name']
        obj=Parcel.objects.filter(type=1)
        if City=="":
            CityList=[]
            
            for i in obj:
                CityList.append({"id" : i.id, "name":i.name})
                
            
            return JsonResponse(CityList, safe=False)

        obj=get_object_or_404(obj,name=City)
        
        data=serialize('geojson',[obj],geometry_field='poly')
        
        return HttpResponse(data)

class Country(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, format=None):
        Country=request.query_params['Name']
        obj=Parcel.objects.filter(type=2)
        if Country=="":
            CountryList=[]
            
            for i in obj:
                CountryList.append({"id" : i.id, "name":i.name})
                
            
            return JsonResponse(CountryList, safe=False)

        obj=get_object_or_404(obj,Name=Country)
        
        data=serialize('geojson',[obj],geometry_field='poly')
        
        return HttpResponse(data)






class Test(APIView):
    permission_classes = (AllowAny, )
    def get(self, request, format=None):
       
        #delparcels()
        #PutCountriesToDatabase()
        #PutCitiesToDatabase()
        return HttpResponse('OK')

class Raster(APIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, format=None):
        cId=request.query_params['cparcel']
        CP=CustomerParcel.objects.get(id=cId)
        geom=CP.poly
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
            asd=MemoryFile(tif_data.tobytes())
            asdf=asd.open()
        
            data=asdf.read(1)
        #delete values if they are not in the polygon
            data=np.ma.masked_where(data<-1500,data)
            #write data to file
            with rasterio.open('test.tif', 'w', driver='GTiff',
                                 height=asdf.height, width=asdf.width, count=1,
                                    dtype=asdf.dtypes[0],
                                    crs={'init': 'epsg:4326'},
                                    transform=asdf.transform) as dst:
                dst.write(data,1)

            #send file to api endpoint
            return HttpResponse(open('test.tif', 'rb'), content_type='image/png')
            
            
             
            
            
            

        #return test.tif file
        

        
            
            
            
            

        return HttpResponse('OK')
            
            
            

            
        
        


        