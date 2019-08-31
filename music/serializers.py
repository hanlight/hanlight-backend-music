from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from .models import Music, Album


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('name', 'album_id', 'artist', 'image_url', )


class MusicListSerializer(serializers.ModelSerializer):
    album = AlbumSerializer(read_only=True)

    class Meta:
        model = Music
        fields = ('title', 'album', )


class MusicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ('title', 'album', 'token', )

    def to_representation(self, instance):
        serializer = super(MusicCreateSerializer, self).to_representation(instance)
        serializer.pop('token')

        album = Album.objects.get(id=serializer['album'])
        serializer['album'] = AlbumSerializer(album).data

        return serializer
