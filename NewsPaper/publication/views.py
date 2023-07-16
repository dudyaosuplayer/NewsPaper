from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Author, Category, Post, PostCategory, Comment
from .filters import PostFilter
from .forms import PostForm
from django.core.mail import EmailMultiAlternatives, send_mail
from static.config import DEFAULT_FROM_EMAIL


class PostsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-time_create')
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news_search'
    ordering = ['-time_create']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    template_name = 'add.html'
    form_class = PostForm
    permission_required = ('publication.add_post')


class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'add.html'
    form_class = PostForm
    permission_required = ('publication.change_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class NewsCategoryView(ListView):
    model = Category
    template_name = 'category/categories.html'
    context_object_name = 'categories'
    queryset = Category.objects.all()


def CategoryDetailView(request, pk):
    category = Category.objects.get(pk=pk)
    is_subscribed = True if len(category.subscribers.filter(id=request.user.id)) else False

    return render(
        request,
        'category/category.html',
        {
            'category': category,
            'is_subscribed': is_subscribed,
            'subscribers': category.subscribers.all()
        }
    )


@login_required
def UnsubscribeCategory(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)

    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(request.user.id)
        result = 'Unsubscribed'

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def SubscribeCategory(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)

    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        email = user.email
        print(email)
        html = render_to_string(
            'mailing/subscribed_to_cat_notification.html',
            {
                'category': category,
                'user': user,
            },
        )

        msg = EmailMultiAlternatives(
            subject=f'Подтверждение подписи на категорию - {category.category_name}',
            body='',
            from_email=DEFAULT_FROM_EMAIL,
            to=[email, ],  # это то же, что и recipients_list - передаем коллекцию
        )

        msg.attach_alternative(html, 'text/html')
        try:
            msg.send()  # отсылаем
        except Exception as e:
            print(e)
        redirect(request.META.get('HTTP_REFERER'))
        # return redirect('')

    return redirect(request.META.get('HTTP_REFERER'))


class СategoryCreateView(CreateView):
    model = Category
    template_name = 'category/category_create.html'
    fields = '__all__'
    # form_class = PostForm
    success_url = '/'
