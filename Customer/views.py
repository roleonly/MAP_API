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
    permission_classes = (AllowAny, )
    def get(self, request, format=None):
        City=request.query_params['Name']
        obj=Parcel.objects.filter(type=1)
        if City=="":
            CityList=[]
            
            for i in obj:
                CityList.append({"id" : i.id, "name":i.Name})
                
            
            return JsonResponse(CityList, safe=False)

        obj=get_object_or_404(obj,Name=City)
        
        data=serialize('geojson',[obj],geometry_field='poly')
        
        return JsonResponse(data,status=201)

class Country(APIView):
    permission_classes = (AllowAny, )
    def get(self, request, format=None):
        Country=request.query_params['Name']
        obj=Parcel.objects.filter(type=2)
        if Country=="":
            CountryList=[]
            
            for i in obj:
                CountryList.append({"id" : i.id, "name":i.Name})
                
            
            return JsonResponse(CountryList, safe=False)

        obj=get_object_or_404(obj,Name=Country)
        
        data=serialize('geojson',[obj],geometry_field='poly')
        
        return JsonResponse(data,status=201)


class Test(APIView):
    permission_classes = (AllowAny, )
    def get(self, request, format=None):
       
        #delparcels()
        #PutCountriesToDatabase()
        #PutCitiesToDatabase()
        return HttpResponse('OK')

