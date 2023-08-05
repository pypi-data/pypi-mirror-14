# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals
from django import template
from textbin import __version__

register = template.Library()

@register.simple_tag(takes_context=False)
def appname():
    return "Django-Textbin v" + __version__

