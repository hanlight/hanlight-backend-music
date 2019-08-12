from rest_framework.routers import DefaultRouter

from .views import MusicViewSet


router = DefaultRouter()
router.register('', MusicViewSet)

urlpatterns = router.urls