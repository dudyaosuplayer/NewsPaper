from django.views.generic import ListView, DetailView
from .models import Author, Category, Post, PostCategory, Comment
from datetime import datetime


class PostsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-time_create')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['time_now'] = datetime.utcnow()
    #     return context


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'post'
