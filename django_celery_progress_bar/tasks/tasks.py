from time import sleep

from config import celery_app


@celery_app.task(name="dummy_counter_task")
def dummy_counter_task():
    print("Counting to 10:")
    for i in range(1, 11):
        print(i)
        sleep(1)
    print("Finished counting!")
