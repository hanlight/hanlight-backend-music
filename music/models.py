from django.db import models


class Album(models.Model):
    album_id = models.PositiveIntegerField()
    name = models.CharField(max_length=150)
    artist = models.CharField(max_length=100)
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{name} - ({artist}, {id})".format(name=self.name, artist=self.artist, id=self.album_id)


class Music(models.Model):
    title = models.CharField(max_length=300)
    album = models.ForeignKey(Album, on_delete=models.PROTECT, related_name='albums')
    token = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{title} - {artist} ({album})".format(title=self.title, artist=self.album.artist, album=self.album.name)