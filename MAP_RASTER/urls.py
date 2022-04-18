



from MAP_RASTER.views import GetRasterImage
from django.urls import path



urlpatterns = [
     
    

    path('tif/', GetRasterImage.as_view(), name='tif'),

]