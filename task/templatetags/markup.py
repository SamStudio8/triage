# http://www.dominicrodger.com/django-markdown.html
from markdown import markdown

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def markup_markdown(value):
    extensions = ["nl2br", ]
    return mark_safe(markdown(force_unicode(value),
                                       extensions,
                                       safe_mode=True,
                                       enable_attributes=False))

