import logging
from datetime import timezone, datetime
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.shortcuts import render
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.mail import EmailMultiAlternatives
from project16012024.news.models import Post, Category

logger = logging.getLogger(__name__)


def my_job(last_week=None, categories=None):
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    post = Post.objects.filter(time_in__sd_s=last_week)
    subscribers = set(Category.objects.filter(catygory=categories).value('subscribers__email', flat=True))

    html_lists = render(
        'post_edit.html', {
            'links': settings.SITE.URL,
            'posts': post,
        }

    )
    msg = EmailMultiAlternatives(
        subject='Новости IT за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_lists, 'html/text')
    msg.send()


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "start apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(my_job, trigger=CronTrigger(second="*/10"), id="my_job", max_instances=1,
                          replace_existing=True, )
        logger.info("Added job 'my_job'.")
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="30"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
