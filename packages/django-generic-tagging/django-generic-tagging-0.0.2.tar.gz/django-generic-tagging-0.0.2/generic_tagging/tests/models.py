from django.db import models


class TagTestArticle0(models.Model):
    title = models.CharField('Title', max_length=255)

    class Meta:
        app_label = 'generic_tagging'


class TagTestArticle1(models.Model):
    title = models.CharField('Title', max_length=255)

    class Meta:
        app_label = 'generic_tagging'
