
from MAP_AUTH.views import LogoutView,RegisterView,Test
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
     
    # jwt token login
    path('token/login/', TokenObtainPairView.as_view(), name='token_login'),                   
    # jwt token refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),                 
    # jwt token logout
    path('token/logout/', LogoutView.as_view(), name='auth_logout'),                          
    
    # from views.py
    path('register/', RegisterView.as_view(), name='auth_register'),  

   
    path('test/', Test.as_view(), name='test'),
]