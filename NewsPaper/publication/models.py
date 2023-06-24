from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user_rate = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        # Расчет суммарного рейтинга статей автора
        post_rate = self.post_set.aggregate(sum_post_rate=Sum('rate'))['sum_post_rate'] * 3
        # Расчет суммарного рейтинга всех комментариев автора
        comment_rate = self.user.comment_set.aggregate(sum_comment_rate=Sum('comment_rate'))['sum_comment_rate']
        # Расчет суммарного рейтинга всех комментариев к статьям автора
        sum_com_rate = self.post_set.annotate(sum_com_rate=Sum('comment__comment_rate')).aggregate(
            sum_com_post_rate=Sum('sum_com_rate'))['sum_com_post_rate']

        self.user_rate = post_rate + comment_rate + sum_com_rate

        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    article = 'article'
    news = 'news'

    PUBLICATIONS = [
        (article, 'статья'),
        (news, 'новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    choice = models.CharField(max_length=7, choices=PUBLICATIONS, default=news)
    time_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.TextField()
    text = models.TextField()
    rate = models.IntegerField(default=0)

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()

    def preview(self):
        return self.text[:123] + '...'

    def __str__(self):
        return f'{self.header.title()}: {self.text.title()}'

    def get_absolute_url(self):
        return f'/news/{self.id}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_rate = models.IntegerField(default=0)

    def __str__(self):
        return self.post.author.user.username

    def like(self):
        self.comment_rate += 1
        self.save()

    def dislike(self):
        self.comment_rate -= 1
        self.save()
