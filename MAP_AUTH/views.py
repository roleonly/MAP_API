


from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from MAP_AUTH.serializer import AuthRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema

from django.http import HttpResponse, JsonResponse

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(APIView):
    permission_classes = (AllowAny,)
    @swagger_auto_schema( request_body=AuthRegisterSerializer)
    def post(self, request):
        serializer=AuthRegisterSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            try:
                user=serializer.save()
            
                token=get_tokens_for_user(user)
                
                print(token)
                return Response(token, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST)





import json
from MAP_PARCEL.models import Parcel
from django.contrib.gis.geos import fromstr

from django.contrib.gis.geos import MultiPolygon
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
            countryMap.poly=MultiPolygon(   fromstr(json.dumps(i['geometry'])   ))
            
            
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
            city.poly=MultiPolygon(   fromstr(json.dumps(i['geometry'])   ))
            
            
        city.save()

def delparcels():
    parcels=Parcel.objects.all()
    for i in parcels:
        i.delete()
class Test(APIView):
   
    
    def post(self,request):
        permission_classes = (IsAuthenticated,)
        delparcels()
        PutCitiesToDatabase()
        PutCountriesToDatabase()
        return JsonResponse({},status=200)



