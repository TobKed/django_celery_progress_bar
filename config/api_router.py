from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from django_celery_progress_bar.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = router.urls
