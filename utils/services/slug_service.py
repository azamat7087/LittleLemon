from django.utils.text import slugify
import transliterate
import random


def gen_slug(s):
    if has_cyr(s):
        s = transliterate.translit(s, reversed=True)
    new_slug = slugify(s, allow_unicode=True)

    return new_slug + "-" + str(random.randint(0, 100))


def has_cyr(s):
    lower = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    return lower.intersection(s.lower()) != set()