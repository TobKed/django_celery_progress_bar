import itertools

import celery
from django.contrib import messages
from django.shortcuts import render

from config import celery_app


def celery_tasks_view(request):
    celery_inspect = celery.task.control.inspect()
    task_ids = None
    if celery_inspect:
        tasks = celery_inspect.registered_tasks()
        task_ids = (
            sorted(list(itertools.chain.from_iterable(tasks.values())))
            if tasks
            else None
        )

    if request.method == "POST":
        task_id = request.POST.get("task_id")

        if not task_id:
            messages.error(request, "task_id should be specified")
        elif task_id not in task_ids:
            messages.error(request, "task_id should be specified")
        else:
            celery_app.send_task(task_id)
            messages.success(request, "Task '{}' triggered!".format(task_id))

    return render(request, "tasks.html", {"task_ids": task_ids})
