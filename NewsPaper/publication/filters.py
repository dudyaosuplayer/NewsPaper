from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'time_create': ['gt'],
            'header': ['icontains'],
            'author': ['in']
        }