from django.forms import ModelForm, BooleanField, Select, CharField
from .models import Post, Author


class PostForm(ModelForm):
    check_box = BooleanField(label='Я подтверждаю достоверность данных')
    class Meta:
        model = Post
        fields = ['title', 'category', 'text']
        labels = {
            'type': 'Тип',
            'category': 'Категория',
            'title': 'Заголовок',
            'text': 'Текст',
        }
        author = CharField(label='Автор', required=False)


