import os
from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='censor')
def censor(value):
    # file_path = os.path.join(settings.STATICFILES_DIRS[0], 'ban_words.txt')
    # with open(file_path, 'r') as file:
    #     words = [word.rstrip('\n') for word in file.readlines()]
    words = ['жопа', 'из-за', ]

    censored_string = value

    for word in words:
        censored_string = censored_string.replace(word, '***')

    return censored_string

