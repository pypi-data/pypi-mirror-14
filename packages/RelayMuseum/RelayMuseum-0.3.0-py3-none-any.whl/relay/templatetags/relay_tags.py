from django import template
from django.conf import settings
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from nano.tools.templatetags.nano_tags import integer, fraction

import logging
_LOG = logging.getLogger(__name__)

register = template.Library()

integer = register.filter(integer)
fraction = register.filter(fraction)

@register.filter
def show_torchfile(torchfile, autoescape=None):
#     if not settings.media_url:
#         return none
#     if torchfile.mimetype == 'text/plain':
#         if autoescape:
#             esc = conditional_escape
#         else:
#             esc = lambda x: x
#         return mark_safe('<pre>%s</pre>' % esc(torchfile.filename.path))

    MEDIA_URL = settings.MEDIA_URL
    title = u'%s of %s' % (torchfile.category_name, torchfile.torch)
    path = u'%s%s' % (MEDIA_URL, torchfile.filename.name)
    if torchfile.mimetype.startswith('image/'):
        return mark_safe('<img title="%s" src="%s" />' % (title, path))
    else:
        return mark_safe(u'<a title="%s" href="%s">%s</a>' % (title, path, torchfile.mimetype))
    assert False, '4'
show_torchfile.needs_autoescape = True
