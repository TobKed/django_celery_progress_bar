from time import sleep

from celery import current_task

from config import celery_app


@celery_app.task(name="dummy_counter_task")
def dummy_counter_task(count_to=10, *args, **kwargs):
    print("Counting to {}: ".format(count_to))
    print("args: {}".format(args))
    print("kwargs: {}".format(kwargs))

    for i in range(1, count_to + 1):
        sleep(1)
        print("{}/{}".format(i, count_to))
        current_task.update_state(
            state="PROGRESS", meta={"current": i, "total": count_to}
        )

    print("Finished counting!")

    return {
        "current": 100,
        "total": 100,
        "status": "Task completed!",
        "result": count_to,
    }
