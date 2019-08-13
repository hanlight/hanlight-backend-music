import jwt

from django.utils import timezone

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins, status

from .crawling.music_search import MusicSearch
from .models import Music, Album
from .serializers import MusicCreateSerializer, MusicListSerializer
from .permissions import IsAuthenticated
from .exceptions import *


class MusicViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Music.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'create':
            return MusicCreateSerializer
        elif self.action == 'list':
            return MusicListSerializer

    def create(self, request, *args, **kwargs):
        today = timezone.now()

        # music apply time check
        if today.hour < 8:
            raise MusicApplyTimeTooEarlyException
        elif today.hour >= 12:
            raise MusicApplyTimeTooLateException

        # Todo: write transaction logic
        today_musics = Music.objects.filter(created_at__year=today.year, created_at__month=today.month,
                                            created_at__day=today.day)

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

    @action(detail=False, methods=['POST'])
    def search(self, request):
        name = request.POST.get('q', None)
        search_type = request.POST.get('type', None)

        data_list = MusicSearch(name, search_type).get_data()

        return Response({
            'success': True,
            'data': {
                'musics': data_list,
            }
        })
