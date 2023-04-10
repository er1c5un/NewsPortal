from django import template

register = template.Library()

RATE_SYMBOLS = {
    'sun': 'солнц',
    'stars': 'звезд',
}


@register.filter()
def rate(value, code='stars'):
    """
   value: значение, к которому нужно применить фильтр
   code: код валюты
   """
    postfix = RATE_SYMBOLS[code]

    return f'{value} {postfix}'


@register.filter()
def censor(value):
    """
   value: значение, к которому нужно применить фильтр
   """
    words_list = value.split()
    # бежим по каждому слову
    for word in words_list:
        if any(symbol.isupper() for symbol in word[1:]):
            index_of_censor_word = words_list.index(word)
            words_list[index_of_censor_word] = word[0] + '*'*(len(word) - 1)

    value = ' '.join(words_list)

    return f'{value}'
