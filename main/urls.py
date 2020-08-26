from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path("", views.homepage, name="home_page"),
    path("register/", views.register, name="register"),
]