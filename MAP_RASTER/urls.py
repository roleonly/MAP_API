



from MAP_RASTER.views import GetRasterImage,GetColoredImages
from django.urls import path



urlpatterns = [
     
    

    path('tif/', GetRasterImage.as_view(), name='tif'),
    path('png/', GetColoredImages.as_view(), name='png'),
]