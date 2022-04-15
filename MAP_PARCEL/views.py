from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from MAP_PARCEL.serializer import ParcelSerializer

from drf_yasg.utils import swagger_auto_schema
from MAP_PARCEL.models import Parcel
from django.http import HttpResponse, JsonResponse



class ParcelView(APIView):
    permission_classes = (IsAuthenticated,)
    
 
    
    def get(self,request):
        
        type=request.GET.get('type')
        if type=='1':
            parcels=Parcel.objects.filter(type=1)
            return JsonResponse({"parcels":list(parcels.values())},safe=False)
        elif type=='2':
            parcels=Parcel.objects.filter(type=2)
            return JsonResponse({"parcels":list(parcels.values())},safe=False)
        elif type=='3':
            parcels=Parcel.objects.filter(owner=request.user)
            try:
                serializer=ParcelSerializer(parcels,many=True)
                return JsonResponse(serializer.data,safe=False)
            except Exception as e:
                return JsonResponse({},safe=False)
        else:
            return JsonResponse({},safe=False)

    @swagger_auto_schema(request_body=ParcelSerializer)
    def post(self,request):
        serializer=ParcelSerializer(data=request.data)
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


