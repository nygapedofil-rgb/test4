from django.urls import path
from . import views


urlpatterns = [
    path('api/login', views.api_login),
    path('api/update_file', views.api_update_file),
    path('api/stream_bytes', views.stream_bytes),
]