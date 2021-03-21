from rest_framework.routers import DefaultRouter
from schedules.views import ScheduleViewSet


router = DefaultRouter()
router.register(r'', ScheduleViewSet, basename='schedules')
urlpatterns = router.urls
