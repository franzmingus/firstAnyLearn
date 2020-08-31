from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path("", views.homepage, name="home_page"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
    path("login_or_register/", views.login_or_register, name="login_or_register"),
    path("<single_slug>", views.single_slug)
]