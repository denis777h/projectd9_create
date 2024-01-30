

версия django 4.2.9
http://127.0.0.1:8000/news
http://127.0.0.1:8000/news/?page=2
http://127.0.0.1:8000/admin


Пользователь admin
Пароль 12345678

Был дополнительно установлен пакет ruff для исправления ошибок
переписана функция my_job():

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

удалена ACCOUNT_EMAIL_VERIFICATION


