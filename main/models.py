from django.db import models

from datetime import datetime as dt
# Create your models here.


class Article(models.Model):

    article_title = models.CharField(max_length=200)
    article_content = models.TextField()
    article_publish_time = models.DateTimeField("date published", default=dt.now())
    article_category = models.CharField(max_length=200, default="Uncategorized")
    article_tags = models.CharField(max_length=200)

    def __str__(self):
        return str( self.article_category) + "_" + str( self.article_title )
