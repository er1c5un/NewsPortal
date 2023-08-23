from django.forms import ModelForm, BooleanField
from .models import Post


# Создаём модельную форму
class PostForm(ModelForm):
    check_box = BooleanField(label='Ало, Галочка!')
    # в класс мета, как обычно, надо написать модель, по которой будет строиться форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['title', 'category']



