
from django.urls import path
from .views import *
from . import consumers

app_name = 'imageai'

urlpatterns = [
    path('', IndexView.as_view(),name="home"),
    path('user_registration/', user_registration,name="user_registration"),
    path('save_image/', SavePicture.as_view(),name="save_image"),
    path('validate_image/', Validate_Image.as_view(),name="validate_image"),  
    path('face_identify/', FaceIdentificaton.as_view(),name="face_identify"),
]
# routing.py
# from django.urls import re_path


# websocket_urlpatterns = [
#     re_path(r'ws/camera/$', consumers.CameraConsumer.as_asgi()),
# ]

