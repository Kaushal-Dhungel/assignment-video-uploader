from django.urls import path
from .views import *

urlpatterns = [
    path("",VideoListView.as_view(), name = 'listView'),
    path("upload",VideoUploadView.as_view(), name = 'uploadView'),
    path("charges",VideoChargesView.as_view(), name = 'chargesView'),

]