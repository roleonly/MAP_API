


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






class Test(APIView):
   
    
    def post(self,request):
        permission_classes = (IsAuthenticated,)
        
        return JsonResponse({},status=200)



