from django.urls import path, include
from . import views

app_name = 'lists'

urlpatterns = [
    path("", views.home),
]