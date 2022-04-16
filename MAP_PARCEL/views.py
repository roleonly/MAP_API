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

class ParcelView(APIView):
    permission_classes = (IsAuthenticated,)
    
 
    
    def get(self,request):
        
       
        parcels=Parcel.objects.filter(owner=request.user)
        try:
            serializer=ParcelSerializer(parcels,many=True)
            return JsonResponse(serializer.data,safe=False)
        except Exception as e:
            return JsonResponse({},safe=False)
       

    @swagger_auto_schema(request_body=ParcelSerializer)
    def post(self,request):
        parcel=request.data
        parcel['owner']=request.user.id
        serializer=ParcelSerializer(data=parcel)
        
        if serializer.is_valid():
            
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)

    def delete(self,request):
        id=request.GET.get('id')
        parcel=Parcel.objects.get(pk=id)
        if parcel.type==3:
            parcel.delete()
            return JsonResponse({},status=204)
        else:
            return HttpResponse('You can not delete predefined parcels')

class CityView(APIView):
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

class CountryView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, format=None):
        Country=request.query_params['Name']
        obj=Parcel.objects.filter(type=2)
        
        if Country=="":
            CountryList=[]
            
            for i in obj:
                CountryList.append({"id" : i.id, "name":i.name})
                
            
            return JsonResponse(CountryList, safe=False)

        obj=get_object_or_404(obj,name=Country)
        
        data=serialize('geojson',[obj],geometry_field='poly')
        
        return HttpResponse(data)