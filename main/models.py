from django.db import models
from django.urls import reverse
from datetime import datetime as dt
from django.contrib.auth.models import User
# Create your models here.
from PIL import Image

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_role = models.CharField(max_length=100, default="nothing")
    user_dp = models.ImageField(default="default.jpeg", upload_to="profile_pics")

    def __str__(self):
        return str(self.user.username) + " Profile"

    def save(self):
        super().save()

        img = Image.open(self.user_dp.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.user_dp.path)

class BlogArticleCategory(models.Model):

    category_name = models.CharField(max_length=200)
    category_summary = models.CharField(max_length=400)
    category_slug = models.CharField(max_length=100, default=1)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return str(self.category_name)


class BlogArticleSeries(models.Model):

    series_name = models.CharField(max_length=200)
    series_category = models.ForeignKey(BlogArticleCategory,
                                        default=1,
                                        verbose_name="Category",
                                        on_delete=models.SET_DEFAULT)
    series_summary = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = "Series"

    def __str__(self):
        return str(self.series_name)


class BlogArticle(models.Model):

    article_title = models.CharField(max_length=200)
    article_content = models.TextField(max_length=5000)
    article_publish_time = models.DateTimeField("date published", default=dt.now())

    # article_tags = models.CharField(max_length=200)
    article_series = models.ForeignKey(BlogArticleSeries,
                                       default=1,
                                       verbose_name="Series",
                                       on_delete=models.SET_DEFAULT)

    article_slug = models.CharField(max_length=200, default=1)

    def __str__(self):
        return str( self.article_title )

    def get_absolute_url(self):

        return reverse("main:article_view", kwargs={"article_slug" : self.article_slug})
