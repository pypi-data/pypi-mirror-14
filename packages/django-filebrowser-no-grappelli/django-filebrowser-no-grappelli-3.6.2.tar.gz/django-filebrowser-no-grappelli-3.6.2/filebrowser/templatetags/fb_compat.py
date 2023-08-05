# coding: utf-8

from django import VERSION as DJANGO_VERSION
from django import template
from django.contrib.admin.templatetags.admin_static import static


register = template.Library()

# cycle

if DJANGO_VERSION < (1, 9):
    try:  # Import cycle from future for django 1.6+
        from django.templatetags.future import cycle
    except ImportError:
        pass
    else:
        register.tag(cycle)

# url

if DJANGO_VERSION < (1, 5):
    from django.templatetags.future import url
    register.tag(url)


# static

def static_jquery():
    if DJANGO_VERSION < (1, 9):
        return static("admin/js/jquery.min.js")

    return static("admin/js/vendor/jquery/jquery.min.js")

register.simple_tag(static_jquery)


def static_search_icon():
    if DJANGO_VERSION < (1, 9):
        return static("admin/img/icon_searchbox.png")

    return static("admin/img/search.svg")

register.simple_tag(static_search_icon)
