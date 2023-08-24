from django.forms import ModelForm, BooleanField
from .models import Post


class PostForm(ModelForm):
    check_box = BooleanField(label='Я подтверждаю достоверность данных')
    class Meta:
        model = Post
        fields = ['title', 'author', 'category', 'text']



