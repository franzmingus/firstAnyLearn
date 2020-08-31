from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models

from .models import BlogArticle, BlogArticleSeries, BlogArticleCategory
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):

    fieldsets = [
        ("Title/Category", {"fields" : ["article_title", "article_series"]}),
        ("Content", {"fields" : ["article_content"]}),
        ("Other", {"fields" : ["article_publish_time", "article_slug"]})
    ]

    formfield_overrides = {
        models.TextField : { "widget" : TinyMCE() }
    }


# admin.site.register(BlogArticle, admin.ModelAdmin)
admin.site.register(BlogArticleCategory, admin.ModelAdmin)
admin.site.register(BlogArticleSeries, admin.ModelAdmin)
admin.site.register(BlogArticle, ArticleAdmin)
