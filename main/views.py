from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import BlogArticle, BlogArticleCategory, BlogArticleSeries
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import OwnUserCreationForm
# Create your views here.


def homepage(request):
    return render(request=request,
                  template_name="main/home.html",
                  context={"blog_categories": BlogArticleCategory.objects.all})


def single_slug(request, single_slug):

    # Check Category
    blog_categories = [c.category_slug for c in BlogArticleCategory.objects.all()]
    if single_slug in blog_categories:

        this_category = BlogArticleCategory.objects.get(category_slug=single_slug)
        series_from_category = BlogArticleSeries.objects.filter(series_category__category_name=this_category.category_name)

        return render(request,
                      "main/category_page.html",
                      context={"blog_category": this_category,
                               "series_from_category": series_from_category})

    # Check Series
    blog_series = [s.series_name for s in BlogArticleSeries.objects.all()]
    if single_slug in blog_series:

        this_series = BlogArticleSeries.objects.get(series_name=single_slug)
        articles_from_series = BlogArticle.objects.filter(article_series__series_name=this_series.series_name)

        return render(request,
                      "main/series_page.html",
                      context={"blog_series": blog_series,
                               "article_from_series": articles_from_series})

    # Check Article
    blog_article = [b.article_slug for b in BlogArticle.objects.all()]
    if single_slug in blog_article:

        blog_article = BlogArticle.objects.get(article_slug=single_slug)

        articles_from_series = BlogArticle.objects.filter(article_series__series_name=blog_article.article_series.series_name).order_by("article_publish_time")

        blog_article_idx = list(articles_from_series).index(blog_article)

        return render(request,
                      "main/single_blog_article_page.html",
                      context={"single_blog_article": blog_article,
                               "sidebar": articles_from_series,
                               "side_bar_pop_out_index":blog_article_idx})

    return HttpResponse("Nothing found for : " + single_slug)

def register(request):

    if request.method == "POST":

        form = OwnUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, "Your Account has been created for " + username)

            login(request, user)
            messages.info(request, "Logged is as : " + username)

            return redirect("main:home_page")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg} : {form.error_messages[msg]}" )

    form = OwnUserCreationForm

    return render(request,
                  "main/register.html",
                  context={"form":form})


def logout_request(request):

    logout(request)
    messages.info(request, "Logged you out")

    return redirect("main:home_page")


def login_or_register(request):

    form_register = OwnUserCreationForm
    form_login = AuthenticationForm

    return render(request,
                  "main/login_or_register.html",
                  context={"form_register": form_register, "form_login": form_login })


def login_request(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Logged in as " + str(username))
                return redirect("main:home_page")
            else:
                messages.error(request, "Invalid userid password")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg} : {form.error_messages[msg]}" )

    form = AuthenticationForm

    return render(request,
                  "main/login.html",
                  {"form":form})

