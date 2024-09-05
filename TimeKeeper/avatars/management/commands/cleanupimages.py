import logging
import os
import time
from datetime import timedelta
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger


logger = logging.getLogger(__name__)


# Конфигурация
UPLOAD_FOLDER = os.path.join(settings.MEDIA_ROOT, 'formatting_avatars')
FILE_LIFETIME = timedelta(minutes=30)


def my_job():
    """
    Task to deleting old formatted images
    """
    now = time.time()
    # проходимся по объектам в директории
    for filename in os.listdir(UPLOAD_FOLDER):
        # получаем путь каждого до каждого объекта
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        # проверяем, является ли объект файлом
        if os.path.isfile(file_path):
            # определяем возраст файла
            file_age = now - os.path.getctime(file_path)
            # если файл старше FILE_LIFETIME - удаляем его из директории
            if file_age > FILE_LIFETIME.total_seconds():
                os.remove(file_path)
                logger.info(f"Deleted {filename}, age: {timedelta(seconds=file_age)}")


# The `close_old_connections` decorator ensures that database connections,
# that have become unusable or are obsolete, are closed before and after your
# job has run. You should use it to wrap any jobs that you schedule that access
# the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age`
    from the database.
    It helps to prevent the database from filling up with old historical
    records that are no longer useful.

    :param max_age: The maximum length of time to retain historical
                    job execution records. Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(minute="*"),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
