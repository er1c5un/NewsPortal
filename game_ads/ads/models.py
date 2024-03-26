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

    def __str__(self):
        return self.name


class Ad(models.Model):
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='AdCategory')
    title = models.CharField(max_length=255, default='')
    #  сделать поле текста с контентом (видео, аудио, картинки...)
    text = models.TextField()

    def __str__(self):
        return f'Объявление {self.title}: {self.text[:15]}'


class AdCategory(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=0)


class Response(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, default=0)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        return user


if __name__ == "__main__":
    pass
