from django.forms import ModelForm, BooleanField, CharField
from .models import Ad


class AdForm(ModelForm):
    check_box = BooleanField(label='Всё правильно')
    class Meta:
        model = Ad
        fields = ['title', 'category', 'text']
        labels = {
            'category': 'Категория',
            'title': 'Заголовок',
            'text': 'Текст',
        }
        author = CharField(label='Автор', required=False)


