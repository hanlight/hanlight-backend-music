from django.urls import (
    include,
    path,
)

from music.urls import router


urlpatterns = [
    path('music/', include(router.urls)),
]