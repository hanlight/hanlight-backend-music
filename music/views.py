import jwt

from django.utils import timezone
from django.conf import settings

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins, status

from .crawling.music_search import MusicSearch
from .models import Music, Adlbum
from .serializers import MusicCreateSerializer, MusicListSerializer
from .permissions import IsAuthenticated
from .exceptions import *


class MusicViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    today = timezone.now()
    queryset = Music.objects.filter(created_at__year=today.year, created_at__month=today.month,
                                            created_at__day=today.day)
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'create':
            return MusicCreateSerializer
        elif self.action == 'list':
            return MusicListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'success': True,
            'data': {
                'musics': serializer.data
            }
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        # music apply time check
        if not settings.DEBUG:  # Todo: Delete when service lunching
            if self.today.hour < 8:
                raise MusicApplyTimeTooEarlyException
            elif self.today.hour >= 12:
                raise MusicApplyTimeTooLateException

        # Todo: write transaction logic
        today_musics = Music.objects.filter(created_at__year=self.today.year, created_at__month=self.today.month,
                                            created_at__day=self.today.day)

        # applied music counting and raise exception
        if today_musics.count() >= 7:
            raise MusicApplyException

        # ( jwt token decoding && get album instance using album_id ) and add data into request
        music_title = request.data['title']
        music_album = request.data['album']

        token = jwt.decode(request.META.get('HTTP_ACCESSTOKEN', None), None, None)['pk']
        obj = Album.objects.get(album_id=music_album)

        for music in today_musics:  # checking is user already applied && is music already applied
            if music.token == token:
                raise UserAlreadyAppliedException
            if music_title == music.title:
                if int(music_album) == music.album.album_id:
                    raise MusicAlreadyAppliedException
        request.data['token'] = token
        request.data['album'] = obj.id

        # Create Music Instance
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'success': True,
            'data': {
                'music': serializer.data
            }
        }, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['GET'])
    def search(self, request):
        name = request.GET.get('q', None)
        search_type = request.GET.get('type', None)

        data_list = MusicSearch(name, search_type).get_data()

        return Response({
            'success': True,
            'data': {
                'musics': data_list,
            }
        }, status=status.HTTP_200_OK)
