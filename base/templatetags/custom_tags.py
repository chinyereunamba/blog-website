from django import template
from django.template.defaultfilters import stringfilter
from ..models import *

register = template.Library()


@register.filter
@stringfilter
def upto(value, delimiter=None):
    return value.split(delimiter)[0]

@register.simple_tag()
def postCount():
    category = Category.objects.all()
    for item in category:
        post = Post.objects.filter(category=item).count()
        return post
    