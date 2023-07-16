from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import PostCategory, Post
from NewsPaper.settings import DEFAULT_FROM_EMAIL


@receiver(m2m_changed, sender=Post.category.through)
def new_post_notify_user(sender, instance, action, **kwargs):
    # Новая статья была создана
    if action == 'post_add':
        subscribers = instance.category.values(
            'subscribers__email', 'subscribers__username'
        )
        for subscriber in subscribers:
            # email = subscriber['subscribers__email']
            # Генерация HTML-сообщения из шаблона
            html = render_to_string(
                'mailing/new_post_notification.html',
                {
                    # 'category': category,
                    'post': instance,
                },
            )

            msg = EmailMultiAlternatives(
                subject=f'Здравствуй, {subscriber.get("subscribers__username")}. Новая статья в твоём любимом разделе!',
                body='',
                from_email=DEFAULT_FROM_EMAIL,
                to=[subscriber.get("subscribers__email")],
            )

            msg.attach_alternative(html, 'text/html')
            try:
                msg.send()
            except Exception as e:
                print(e)
