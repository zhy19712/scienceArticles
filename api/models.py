from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    token = models.CharField(max_length=255)


class Target(models.Model):
    url = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    type = models.IntegerField()
    remark = models.CharField(max_length=255, null=True)


class Article(models.Model):
    domain = models.URLField(max_length=255)
    url = models.URLField(max_length=255)
    title = models.CharField(max_length=255)
    time = models.CharField(max_length=255, null=True)
    text = models.TextField(null=True)


class Keyword(models.Model):
    keyword = models.CharField(max_length=255, null=True)
    type = models.IntegerField()


class ScrapedUrls(models.Model):
    url = models.CharField(max_length=255, null=True)
