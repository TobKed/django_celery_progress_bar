from django.urls import path

from django_celery_progress_bar.tasks.views import (
    celery_tasks_view,
    celery_tasks_with_progress_view,
    get_progress_view,
)

app_name = "tasks"
urlpatterns = [
    path("list/", celery_tasks_view, name="celery_tasks_view"),
    path(
        "list_progress/",
        celery_tasks_with_progress_view,
        name="celery_tasks_with_progress_view",
    ),
    path("progress/<str:task_id>/", get_progress_view, name="get_progress_view"),
]
