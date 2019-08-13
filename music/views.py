from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins, status

from .crawling.music_search import MusicSearch

from .models import Music, Album
from .serializers import MusicCreateSerializer, MusicListSerializer
from .permissions import IsAuthenticated


class MusicViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Music.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'create':
            return MusicCreateSerializer
        elif self.action == 'list':
            return MusicListSerializer

    def create(self, request, *args, **kwargs):
        obj = Album.objects.get(album_id=request.data['album'])
        request.data['album'] = obj.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['POST'])
    def search(self, request):
        name = request.POST.get('q', None)
        search_type = request.POST.get('type', None)

        data_list = MusicSearch(name, search_type).get_data()

        return Response({
            'data': data_list,
        })