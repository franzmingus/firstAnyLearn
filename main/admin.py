from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models

from .models import Article
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):

    fieldsets = [
        ("Title/Category", {"fields" : ["article_title", "article_category"]}),
        ("Content", {"fields" : ["article_content"]}),
        ("Other", {"fields" : ["article_publish_time","article_tags"]})
    ]

    formfield_overrides = {
        models.TextField : { "widget" : TinyMCE() }
    }

admin.site.register(Article, ArticleAdmin)
