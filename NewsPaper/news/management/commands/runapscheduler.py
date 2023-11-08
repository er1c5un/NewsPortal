import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from ...models import Post, CategorySubscribers, Category, Author
logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def week_mail_to_subscriptors():
    #  Your job processing logic here...
    print('hello from job "week_mail_to_subscriptors"')
    categories = Category.objects.all()
    category_posts = {}
    for category in categories:
        posts = Post.objects.filter(postcategory__category=category, were_sent_on_weekly_mails=False)
        category_posts[category] = posts
        if len(posts) > 0:
            message = ""
            for post in posts:
                message = f"{message}\n{post.title}"
            subscribers = CategorySubscribers.objects.filter(category=category)
            email_list = []
            for sub in subscribers:
                email_list.append(sub.user.email)
            # отправляем письмо всем админам по аналогии с send_mail, только здесь получателя указывать не надо
            send_mail(
                subject=f'Еженедельная рассылка',  # имя клиента и дата записи будут в теме для удобства
                message=f"{message}",  # сообщение с кратким описанием проблемы
                from_email='er1c5un@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
                recipient_list=email_list  # здесь список получателей. Например, секретарь, сам врач и т. д.
            )
            Post.objects.filter(postcategory__category=category).update(were_sent_on_weekly_mails=True)

# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            week_mail_to_subscriptors,
            #trigger=CronTrigger(day_of_week="fri", hour="17", minute="00"),
            trigger=CronTrigger(second="*/30"),
            id="week_mail_to_subscriptors",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'week_mail_to_subscriptors'.")

        # scheduler.add_job(
        #     delete_old_job_executions,
        #     trigger=CronTrigger(
        #         day_of_week="mon", hour="00", minute="00"
        #     ),
        #     # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
        #     id="delete_old_job_executions",
        #     max_instances=1,
        #     replace_existing=True,
        # )
        # logger.info(
        #     "Added weekly job: 'delete_old_job_executions'."
        # )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")