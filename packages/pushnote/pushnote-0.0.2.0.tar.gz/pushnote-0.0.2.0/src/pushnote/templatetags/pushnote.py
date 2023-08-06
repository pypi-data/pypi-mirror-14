from django import template
from ..utils import tokenize

register = template.Library()


@register.simple_tag(takes_context=True)
def pushnote_token(context):
    user = context['user']
    try:
        return tokenize(user)
    except:
        return False
