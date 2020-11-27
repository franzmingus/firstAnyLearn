from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from .models import BlogArticle, BlogArticleCategory, BlogArticleSeries
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import OwnUserCreationForm, MyUserCreationForm, UserUpdateForm, ProfileUpdateForm

from django.views.generic import ListView, DetailView, CreateView


#Class based Views

class HomeListView(ListView):
    model = BlogArticleCategory
    template_name = "main/home.html"
    context_object_name = "blog_categories"
    ordering = ["category_name"]


class ArticleDetailView(DetailView):
    model = BlogArticle
    context_object_name = "single_blog_article"

    def get_object(self):
        return get_object_or_404(BlogArticle, article_slug=self.kwargs['article_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        blog_article = self.get_object()
        print(blog_article.article_title)
        articles_from_series = BlogArticle.objects.filter(article_series__series_name=blog_article.article_series.series_name)\
                                .order_by("article_publish_time")

        blog_article_idx = list(articles_from_series).index(blog_article)

        context["sidebar"] = articles_from_series
        context["side_bar_pop_out_index"] = blog_article_idx

        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = BlogArticle
    fields = ["article_title", "article_content", "article_series", "article_slug"]





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

        print("Returning Category Page")
        return render(request,
                      "main/category_page.html",
                      context={"blog_category": this_category,
                               "series_from_category": series_from_category})

    # Check Series
    blog_series = [s.series_name for s in BlogArticleSeries.objects.all()]
    if single_slug in blog_series:

        this_series = BlogArticleSeries.objects.get(series_name=single_slug)
        articles_from_series = BlogArticle.objects.filter(article_series__series_name=this_series.series_name)

        print("Returning Series Page")
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

        print("Returning Blog Page")
        return render(request,
                      "main/single_blog_article_page.html",
                      context={"single_blog_article": blog_article,
                               "sidebar": articles_from_series,
                               "side_bar_pop_out_index":blog_article_idx})

    return HttpResponse("Nothing found for : " + single_slug)


def register(request):

    if request.method == "POST":

        form = MyUserCreationForm(request.POST)

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

    form = MyUserCreationForm

    return render(request,
                  "main/register.html",
                  context={"form": form})


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
                  {"form": form})

@login_required
def profile(request):
    if request.method == "POST":
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()

            messages.success(request, "Updated")
            return redirect("main:profile")



    elif request.method == "GET":
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            "user_update_form": user_update_form,
            "profile_update_form": profile_update_form
        }

        return render(request,
                      "main/profile.html",
                      context=context)

