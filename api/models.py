from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    token = models.CharField(max_length=255)


class Center(models.Model):
    name = models.CharField(max_length=255)
    uid  = models.IntegerField()


class Target(models.Model):
    url = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    type = models.IntegerField(null=True)
    remark = models.CharField(max_length=255, null=True)
    status = models.IntegerField(null=True)
    last_crawled_time = models.CharField(max_length=255, null=True)
    belong = models.CharField(max_length=255, null=True)


class Article(models.Model):
    source = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    time = models.CharField(max_length=255, null=True)
    text = models.TextField(null=True)
    filepath = models.CharField(max_length=255, null=True)
    belong = models.CharField(max_length=255, null=True)


class Keyword(models.Model):
    keyword = models.CharField(max_length=255, null=True)
    type = models.IntegerField()


class ScrapedUrls(models.Model):
    url = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    time = models.CharField(max_length=255, null=True)
