from datetime import datetime

from allauth.account.forms import SignupForm
from django.contrib.auth.models import User, Group
from django.core.cache import cache
from django.db import models

state = 'State'
news = 'News'

types = [
    (state, 'Статья'),
    (news, 'Новость'),
]


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_rate(self):
        author_posts = Post.objects.filter(author=self)
        post_rate_sum = 0
        comment_post_rate_sum = 0
        for post in author_posts:
            post_rate_sum += post.rate
            comments_post = Comment.objects.filter(post=post)
            for comment in comments_post:
                comment_post_rate_sum += comment.rate

        post_rate_sum *= 3

        author_comments = Comment.objects.filter(user=self.user)
        comment_author_rate_sum = 0
        for comment in author_comments:
            comment_author_rate_sum += comment.rate
        self.rate = post_rate_sum + comment_author_rate_sum + comment_post_rate_sum


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='CategorySubscribers')

    def __str__(self):
        return self.name


class CategorySubscribers(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=types, default=state)
    create_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255, default='')
    text = models.TextField()
    rate = models.IntegerField(default=0)
    were_sent_on_weekly_mails = models.BooleanField(default=False)

    def __str__(self):
        return f'Пост {self.title}: {self.text[:15]}'

    def like(self):
        self.rate += 1

    def dislike(self):
        new_rate = self.rate - 1
        self.rate = new_rate if new_rate >= 0 else 0

    def preview(self):
        return self.text[:123] + '...' if len(self.text) >= 124 else self.text

    def get_absolute_url(self):
        return f'/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=0)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0)

    def like(self):
        self.rate += 1

    def dislike(self):
        new_rate = self.rate - 1
        self.rate = new_rate if new_rate >= 0 else 0


if __name__ == "__main__":
    pass
