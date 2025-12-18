from django.urls import path,include
from users.views import *
from . import views 
# from app import consumers
from django.urls import reverse

app_name = "users"

urlpatterns = [    
    path('login/', views.user_login, name="login"),
    path('register/', views.user_registration, name='register'),
    path('logout/', views.user_logout, name="logout"),    
]