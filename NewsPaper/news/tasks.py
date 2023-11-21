from celery import shared_task
import time

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import CategorySubscribers, Post, Category


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")

@shared_task
def send_email_to_subscribers_of_new_post(category_id, post_id):
    post = Post.objects.get(id=post_id)
    subscribers = CategorySubscribers.objects.filter(category=category_id)
    email_list = []
    for sub in subscribers:
        email_list.append(sub.user.email)
    context = {
        'post': post,
    }
    html_message = render_to_string('account/email/email_new_post.html', context)
    plain_message = strip_tags(html_message)
    # отправляем письмо всем админам по аналогии с send_mail, только здесь получателя указывать не надо
    send_mail(
        subject=f'{post.title}',  # имя клиента и дата записи будут в теме для удобства
        message=plain_message,  # сообщение с кратким описанием проблемы
        from_email='er1c5un@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
        recipient_list=email_list,  # здесь список получателей. Например, секретарь, сам врач и т. д.
        html_message=html_message,
    )


@shared_task
def week_mail_to_subscribers():
    print('hello from task "week_mail_to_subscribers"')
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

            context = {
                'posts': posts,
            }

            html_message = render_to_string('account/email/email_weekly_posts.html', context)
            plain_message = strip_tags(html_message)
            print(f"sending mail to email_list: {email_list}")
            send_mail(
                subject='Еженедельная рассылка',
                message=plain_message,
                from_email='er1c5un@yandex.ru',
                recipient_list=email_list,
                html_message=html_message,
            )

            # отправляем письмо всем админам по аналогии с send_mail, только здесь получателя указывать не надо
            # send_mail(
            #     subject=f'Еженедельная рассылка',  # имя клиента и дата записи будут в теме для удобства
            #     message=f"{message}",  # сообщение с кратким описанием проблемы
            #     from_email='er1c5un@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
            #     recipient_list=email_list  # здесь список получателей. Например, секретарь, сам врач и т. д.
            # )
            Post.objects.filter(postcategory__category=category).update(were_sent_on_weekly_mails=True)