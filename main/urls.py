from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path("", views.HomeListView.as_view(), name="home_page"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
    path("login_or_register/", views.login_or_register, name="login_or_register"),
    path("profile/", views.profile, name="profile"),
    path("create_article/", views.ArticleCreateView.as_view(), name="create_article"),
    path("<single_slug>/", views.single_slug, name="single_slug"),
    path("article/<str:article_slug>/", views.ArticleDetailView.as_view(), name="article_view"),

]