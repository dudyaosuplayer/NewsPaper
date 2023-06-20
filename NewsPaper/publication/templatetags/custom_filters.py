import os
import re
from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='censor')
def censor(value):
    file_path = os.path.join(settings.STATICFILES_DIRS[0], 'ban_words.txt')
    with open(file_path, 'r', encoding='utf-8') as file:
        words = [word.rstrip('\n').lower() for word in file.readlines()]

    censored_string = value

    for word in words:
        pattern = r'\b' + re.escape(word) + r'\b'
        censored_string = re.sub(pattern, '***', censored_string, flags=re.IGNORECASE)

    return censored_string

