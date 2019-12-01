from rest_framework.routers import DefaultRouter

from .views import MusicViewSet


music_router = DefaultRouter()
music_router.register('', MusicViewSet)
