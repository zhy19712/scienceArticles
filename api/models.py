from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
    token = models.CharField(max_length=255, null=True)
    avatar = models.CharField(max_length=255, null=True)
    status = models.IntegerField(null=True)
    center_id = models.IntegerField(null=True)


class System(models.Model):
    scraped_interval = models.IntegerField()


class Center(models.Model):
    center = models.CharField(max_length=255, null=True)


class Category(models.Model):
    center_id = models.IntegerField()
    category = models.CharField(max_length=255)


class Target(models.Model):
    center_id = models.IntegerField()
    target = models.CharField(max_length=255)
    type = models.IntegerField()
    remark = models.CharField(max_length=255, null=True)
    status = models.IntegerField()


class Article(models.Model):
    target = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255, null=True)
    time = models.DateTimeField(null=True)
    text = models.TextField(null=True)
    filepath = models.CharField(max_length=255, null=True)


class Keyword(models.Model):
    category_id = models.IntegerField()
    keyword = models.CharField(max_length=255)
    status = models.IntegerField()


class ScrapedUrls(models.Model):
    target = models.CharField(max_length=255, null=True)
    time = models.CharField(max_length=255, null=True)


class KeywordArticle(models.Model):
    keyword_id = models.IntegerField()
    article_id = models.IntegerField()
