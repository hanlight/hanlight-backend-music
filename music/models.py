from django.db import models


class Album(models.Model):
    name = models.CharField(max_length=150, unique=True)
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Music(models.Model):
    title = models.CharField(max_length=300)
    album = models.ForeignKey(Album, on_delete=models.PROTECT, related_name='albums')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)