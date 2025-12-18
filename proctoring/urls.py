from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("image_ai.urls", namespace='image_ai')),
    path('screen_recorder_app/', include('screen_recorder.urls', namespace='screen_recorder_app')), 
    path('users/', include("users.urls", namespace='users')),
    path('exams/', include("exams.urls", namespace='exams')),    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
