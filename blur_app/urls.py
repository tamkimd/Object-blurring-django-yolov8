from django.urls import path
from .views import process_video

urlpatterns = [
    path('process_video/', process_video, name='process_video'),

]
