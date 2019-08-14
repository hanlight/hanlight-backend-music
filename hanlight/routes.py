from django.urls import (
    include,
    path,
)

from music.routes import music_router


urlpatterns = [
    path('music/', include(music_router.urls)),
]