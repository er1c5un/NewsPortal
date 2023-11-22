from django.contrib import admin

# Register your models here.
from .models import Author, Post, Category, CategorySubscribers, Comment, PostCategory

admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(CategorySubscribers)
admin.site.register(Comment)
admin.site.register(PostCategory)
