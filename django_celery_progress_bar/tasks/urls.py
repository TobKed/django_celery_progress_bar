from django.urls import path

from django_celery_progress_bar.tasks.views import celery_tasks_view

app_name = "tasks"
urlpatterns = [
    path("list/", celery_tasks_view, name="celery_tasks_view"),
]
