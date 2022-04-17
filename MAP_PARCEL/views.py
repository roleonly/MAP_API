from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from MAP_PARCEL.serializer import ParcelSerializer

from drf_yasg.utils import swagger_auto_schema
from MAP_PARCEL.models import Parcel
from django.http import HttpResponse, JsonResponse

from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
import json
from django.contrib.gis.geos import fromstr

from django.contrib.gis.geos import MultiPolygon


class MapParcel(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        
        data=request.data
        newparcel=Parcel()
        newparcel.name='user-'+data['name']
        newparcel.type=data['type']
        
        poly=json.loads(data['poly'])
        
        poly.pop('id')
        if poly['geometry']['type']=="MultiPolygon" :
            poly=json.dumps(poly['geometry'])
            
            
        else:   
            poly=MultiPolygon(   fromstr(json.dumps(poly['geometry'])   ))
        
        newparcel.poly=poly
        newparcel.save()
        newparcel.owner.add(request.user)
        newparcel.save()
        return Response(status=status.HTTP_201_CREATED)
        
        
        
        
        

class ParcelView(APIView):
    permission_classes = (IsAuthenticated,)
    
 
    
   
        
        
    def get(self, request, format=None):
        permission_classes = (IsAuthenticated, )
        
        parcels=Parcel.objects.filter(owner=request.user)       
       
        parcel_list=[]
             
        for i in parcels:
            parcel_list.append({"id" : i.id, "name":i.name})
                
            
        return JsonResponse(parcel_list, safe=False)

        
                  
    

    @swagger_auto_schema(request_body=ParcelSerializer)
    def post(self,request):
        permission_classes = (IsAuthenticated, )
        id=request.GET.get('id')
        parcel=Parcel.objects.get(pk=id)
        parcel.owner.add(request.user)
        parcel.save()
        
       
        
        
        return JsonResponse({'id':parcel.id,'name':parcel.name},status=201,safe=False)
        

    def delete(self,request):
        permission_classes = (IsAuthenticated, )
        id=request.GET.get('id')
        parcel=Parcel.objects.get(pk=id)
        if parcel.type==3:
            parcel.delete()
            return JsonResponse({},status=204)
        else:
            parcel.owner.remove(request.user)
            return JsonResponse({'id':parcel.id,'name':parcel.name},status=201,safe=False)

class CityView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, format=None):
        
        obj=Parcel.objects.filter(type=1)
        
        CityList=[]
            
        for i in obj:
            CityList.append({"id" : i.id, "name":i.name})
                
            
        return JsonResponse(CityList, safe=False)

        

class CountryView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, format=None):
        
        obj=Parcel.objects.filter(type=2)
        
        
        CountryList=[]
            
        for i in obj:
            CountryList.append({"id" : i.id, "name":i.name})
                
            
        return JsonResponse(CountryList, safe=False)

      

class GeometryView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, format=None):
        id=request.GET.get('id')
        obj=get_object_or_404(Parcel,id=id)
        data=serialize('geojson',[obj],geometry_field='poly')
        return HttpResponse(data)