from django.views.generic import ListView, DetailView
from .models import Author, Category, Post, PostCategory, Comment


class PostsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'post'
