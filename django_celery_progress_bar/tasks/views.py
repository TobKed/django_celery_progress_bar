import itertools

import celery
from celery.result import AsyncResult
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from config import celery_app


@login_required
def celery_tasks_view(request):
    celery_inspect = celery.task.control.inspect()
    task_ids = None
    if celery_inspect:
        tasks = celery_inspect.registered_tasks()
        task_ids = (
            sorted(set(itertools.chain.from_iterable(tasks.values())))
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


@login_required
def celery_tasks_with_progress_view(request):
    task_ids = ["dummy_counter_task"]
    task_id = None
    triggered_task_id = None

    if request.method == "POST":
        task_id = request.POST.get("task_id")
        count_to = int(request.POST.get("count_to", "10"))

        if not task_id:
            messages.error(request, "task_id should be specified")
        elif task_id not in task_ids:
            messages.error(request, "task_id should be specified")
        else:
            triggered_task_id = celery_app.send_task(
                task_id, kwargs={"count_to": count_to}, queue="highprio"
            )
            messages.success(
                request, "Task '{}' triggered (count_to: {})!".format(task_id, count_to)
            )
            messages.success(request, "Task id: {}".format(triggered_task_id))

    return render(
        request,
        "trigger.html",
        {
            "task_ids": task_ids,
            "task_id": task_id,
            "triggered_task_id": triggered_task_id,
        },
    )


@login_required
def get_progress_view(request, task_id):
    result = AsyncResult(task_id)

    if result.state == "PENDING":
        response_data = {
            "state": result.state,
            "current": 0,
            "total": 1,
            "status": "Pending...",
        }
    elif result.state != "FAILURE":
        response_data = {
            "state": result.state,
            "current": result.info.get("current", 0),
            "total": result.info.get("total", 1),
            "status": result.info.get("status", ""),
        }
        if "result" in result.info:
            response_data["result"] = result.info["result"]
    else:
        # something went wrong in the background job
        response_data = {
            "state": result.state,
            "current": 1,
            "total": 1,
            "status": str(result.info),  # this is the exception raised
        }

    return JsonResponse(response_data)
