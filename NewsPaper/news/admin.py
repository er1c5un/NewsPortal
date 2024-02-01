from django.contrib import admin

# Register your models here.
from .models import Author, Post, Category, CategorySubscribers, Comment, PostCategory
from modeltranslation.admin import \
    TranslationAdmin  # импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)


class CategoryAdmin(TranslationAdmin):
    model = Category


class AuthorAdmin(TranslationAdmin):
    model = Author


class PostAdmin(TranslationAdmin):
    model = Post


admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(CategorySubscribers)
admin.site.register(Comment)
admin.site.register(PostCategory)
