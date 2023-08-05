# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals
# Django
from django.conf.urls import include, url
from django.contrib import admin
from django.views.i18n import javascript_catalog
# For Django REST api
from rest_framework.urlpatterns import format_suffix_patterns
# Textbin
from . import views


urlpatterns = [
    # Django REST Framework: API
    # --------------------------

    # .../api/posts/
    url(r'^api/$', views.ApiTextCreate.as_view(),
        name='text_api_create'),

    # .../textbin/api/12b29374
    # .../textbin/api/12b29374.api  or *.json
    url(r'^api/(?P<pk>\w+)$', views.ApiTextDetail.as_view(),
        name='text_api_detail'),

    # For authentication
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest')),
    ]

# Allow to specify data format as api/12b29374.api or *.json
urlpatterns = format_suffix_patterns(urlpatterns)

# Add internationalization to JavaScript code
js_info_dict = {'packages': ('textbin',), }
urlpatterns += [
    url(r'^jsi18n/$', javascript_catalog, js_info_dict, name='javascript-catalog'),
]

urlpatterns += [
    url(r'^admin/', include(admin.site.urls)),
    # Create post
    # -----------
    # .../
    url(r'^$', views.TextCreate.as_view(), name='text_create'),
    # View post details
    # -----------------
    # (!) place it last.
    # All unknown urls will be interpreted as post id's (exclude admin and api)
    # .../12b29374
    url(r'^(?!admin|api|api-auth)(?P<pk>\w+)$', views.TextDetail.as_view(),
        name='text_detail'),
    ]
