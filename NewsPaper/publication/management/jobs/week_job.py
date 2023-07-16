from datetime import timedelta
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from publication.models import Post, Category
from static.config import DEFAULT_FROM_EMAIL

def compose_obj(post):
    _post = {}
    _post['id'] = post.id
    _post['title'] = post.header
    return _post


def send_notification(subscriber, cat_obj):
    template = 'mailing/weekly_notification.html'
    subject = f'Еженедельная рассылка новых публикаций'

    posts_info = {"category": '', "posts": []}

    for category, posts in cat_obj.items():
        posts_info["category"] = category
        posts_info["posts"] = [compose_obj(post) for post in posts]
    # print(posts_info["posts"])

    html = render_to_string(
        template_name=template,
        context={
            'user_name': subscriber,
            'posts_info': posts_info,
        },
    )

    msg = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=[subscriber.email, ],
    )
    msg.attach_alternative(html, "text/html")
    msg.send()


def weelky_news_job():
    for category in Category.objects.all():
        mailing_dict = {}  # инициализация переменной, пустой словарь <class 'dict'>
        cat_name = category.category_name
        postsForWeek = Post.objects.filter(category=category, time_create__gte=timezone.now() - timedelta(weeks=1))
        if not postsForWeek:
            continue
            # вычисляем юзеров-подписчиков
        for subscriber in category.subscribers.all():  # берем каждого подписанта
            if subscriber not in mailing_dict:  # если объект юзер еще не содержится в словаре
                mailing_dict[subscriber] = {}  # добавляем объект юзера в качестве ключа, присваиваем value - пустой
                # словарь
            if cat_name not in mailing_dict[subscriber]:  # если категории еще нет
                mailing_dict[subscriber][cat_name] = set()  #
            mailing_dict[subscriber][cat_name].update(postsForWeek)  # обращаемся к ключу вложенного словаря и
            # добавляем в него значение - все посты
            # категории за неделю

        for subscriber, cat_name in mailing_dict.items():
            send_notification(subscriber, cat_name)
