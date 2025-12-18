from django.urls import path
from . import views


app_name = 'screen_recorder_app'

urlpatterns = [
    path('serve_video/<int:media_id>/', views.serve_video, name='serve_video'),   
    path('save_recording/', views.ChunkRecorder.as_view(), name='save_recording'),             
]
