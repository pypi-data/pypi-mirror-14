from django import VERSION as DJANGO_VERSION
from django.contrib.admin.sites import site as admin_site

__all__ = [
    'smart_text',
    'json',
    'admin_context',
    'patterns'
]

# Handle django.utils.encoding rename in 1.5

try:
    from django.utils.encoding import smart_text
except ImportError:
    from django.utils.encoding import smart_unicode as smart_text

# Old python, do we really need it?

try:
    import json
except ImportError:
    from django.utils import simplejson as json

# Django >= 1.8 needs has_permission in context

def admin_context(context, request):
    if DJANGO_VERSION >= (1, 8):
        return dict(admin_site.each_context(request), **context)

    return context

# django.conf.urls.patterns in django 1.9

if DJANGO_VERSION < (1, 9):
    from django.conf.urls import patterns
else:
    def patterns(prefix, *args):
        return list(args)
