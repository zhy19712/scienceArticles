from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    token = models.CharField(max_length=255)


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
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    time = models.CharField(max_length=255, null=True)
    text = models.TextField(null=True)
    filepath = models.CharField(max_length=255, null=True)


class Keyword(models.Model):
    category_id = models.IntegerField()
    keyword = models.CharField(max_length=255)
    type = models.IntegerField()
    status = models.IntegerField()


class ScrapedUrls(models.Model):
    target = models.CharField(max_length=255, null=True)
    time = models.CharField(max_length=255, null=True)


class KeywordArticle(models.Model):
    keyword_id = models.IntegerField()
    article_id = models.IntegerField()
