from datetime import datetime

from allauth.account.forms import SignupForm
from django.contrib.auth.models import User, Group
from django.core.cache import cache
from django.db import models


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    #subscribers = models.ManyToManyField(User, through='CategorySubscribers')

    def __str__(self):
        return self.name


class Ad(models.Model):
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='AdCategory')
    title = models.CharField(max_length=255, default='')
    #  сделать поле текста с контентом (видео, аудио, картинки...)
    text = models.TextField()
    #were_sent_on_weekly_mails = models.BooleanField(default=False)

    def __str__(self):
        return f'Объявление {self.title}: {self.text[:15]}'

    #def like(self):
    #    self.rate += 1

    #def dislike(self):
    #    new_rate = self.rate - 1
    #    self.rate = new_rate if new_rate >= 0 else 0

    #def preview(self):
    #    return self.text[:123] + '...' if len(self.text) >= 124 else self.text

    #def get_absolute_url(self):
    #    return f'/{self.id}'

    #def save(self, *args, **kwargs):
    #    super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
    #    cache.delete(f'post-{self.pk}')


class AdCategory(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=0)


class Response(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, default=0)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        #basic_group = Group.objects.get(name='common')
        #basic_group.user_set.add(user)
        return user


if __name__ == "__main__":
    pass
