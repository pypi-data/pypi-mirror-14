# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals
import six
import random
import string
import urllib
import urlparse
from collections import defaultdict

from django.conf import settings
from django.db import models
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy

# Length of unique hex-key for every text
ID_LENGTH = settings.TEXTBIN.get('ID_LENGTH', 10)


def _unique_id():
    """ Returns unique ID for Text.id """
    check_field = 'id'
    model = Text
    new_id = None
    while True:
        new_id = ''.join(random.choice(
            string.ascii_letters + string.digits) for _ in range(ID_LENGTH))
        try:
            model.objects.get(**{check_field: new_id})
        except ObjectDoesNotExist as err:
            # ID is unique
            break
    return new_id


class MediaType(object):
    """
    Allowed types.
    They also must be listed in `valid_url_media()` function in
    ValidationError in human-readable format.
    DO NOT MODIFY EXIST TYPE NUMBERS.
    """
    UNKNOWN = 0
    IMAGE = 1  # DO NOT MODIFY. USED IN EXTERNAL APPS.
    VIDEO = 2
    YT_VIDEO = 3
    CHOICES = (
        (UNKNOWN, 'Unknown'),
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
        (YT_VIDEO, 'YouTube'),
    )

    @classmethod
    def autodetect(cls, url):
        if not url:
            raise ValueError('Unable to autodetect media type: url is False.')

        # Try to parse YouTube url`s
        youtube_url = cls._get_youtube_embed(url)
        if youtube_url:
            return cls.YT_VIDEO, youtube_url

        # if we reach this line - content type still undefined

        # Get type from page headers
        res = urllib.urlopen(url)
        http_message = res.info()
        # full = http_message.type    # 'text/plain'
        curr_type = http_message.maintype  # 'text'
        curr_type = curr_type.capitalize()
        for choice in cls.CHOICES:
            if curr_type == choice[1]:
                return choice[0], url

        # Try to define type if it has wrong headers: "text"
        if curr_type == 'Text' and url.endswith(
                ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tga',)):
            return cls.IMAGE, url

        # If content type not in cls.CHOICES
        if settings.TEXTBIN.get('ALLOW_UNKNOWN_TYPES', False):
            return cls.UNKNOWN, url
        else:
            raise FieldError('Not supported content type at ' + url)

    @classmethod
    def _get_youtube_embed(cls, url):
        """
        Examples:
        - http://youtu.be/SA2iWivDJiE
        - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
        - http://www.youtube.com/embed/SA2iWivDJiE
        - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
        """
        id = None
        query = urlparse.urlparse(url)
        if query.hostname == 'youtu.be':
            id = query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com'):
            if query.path == '/watch':
                p = urlparse.parse_qs(query.query)
                id = p['v'][0]
            if query.path[:7] == '/embed/':
                id = query.path.split('/')[2]
            if query.path[:3] == '/v/':
                id = query.path.split('/')[2]
        if id:
            url = 'https://www.youtube.com/embed/' + id
        else:  # fail
            url = None
        return url

    @classmethod
    def get_by_name(cls, name):
        # Get type `int` by it`s `str` name
        for choice in cls.CHOICES:
            if name.capitalize() == choice[1]:
                return choice[0]
        return cls.UNKNOWN


def valid_url_media(url):
    try:
        MediaType.autodetect(url)
    except FieldError:
        raise ValidationError(ugettext_lazy(
            'URL must point to one of this: image, video, youtube page'))


@python_2_unicode_compatible
class Text(models.Model):
    len_author = 100  # max length of author_name CharField
    def_author = 'Anonymous'  # Default author name

    id = models.CharField(max_length=ID_LENGTH, primary_key=True,
                          default=_unique_id,
                          editable=False)
    text = models.TextField(default='',
                            blank=True)

    posted_at = models.DateTimeField(auto_now_add=True)
    author_name = models.CharField(max_length=len_author,
                                   default=def_author,
                                   blank=True)
    author_url = models.URLField(blank=True,
                                 default='')

    # Параметры отображения в форме
    widget_labels = dict()
    widget_labels['text'] = _('Text')
    widget_labels['author_name'] = _('Your name')
    widget_labels['author_url'] = _('Homepage')

    widget_placeholders = defaultdict(lambda: '')
    # Не указанные в словаре поля будут иметь пустую строку placeholder
    widget_placeholders['text'] = _('Enter text')

    @property
    def images(self):
        return self.media.filter(type=MediaType.IMAGE)

    @property
    def videos(self):
        return self.media.filter(type__in=[MediaType.VIDEO, MediaType.YT_VIDEO])

    @property
    def unknowns(self):
        return self.media.filter(type=MediaType.UNKNOWN)

    def __str__(self):
        return self.id


class MediaManager(models.Manager):
    def create_media(self, text, url, type_=None):
        # Create Media instance with content type autodetection from url (if
        # not specified)

        # Get type
        if not type_:
            type_, url = MediaType.autodetect(url)
        if isinstance(type_, str) or isinstance(type_, unicode):
             try:
                type_ = int(type_)
             except ValueError:
                type_ = MediaType.get_by_name(type_)
        if not isinstance(type_, int):
            raise ValidationError(ugettext_lazy(
                'Unsupported media type: ' + str(type_)))

        media = self.create(text=text, url=url, type=type_)
        return media


@python_2_unicode_compatible
class Media(models.Model):
    # Objects manager
    objects = MediaManager()

    # Objects attributes
    text = models.ForeignKey(Text,
                             editable=False,
                             verbose_name='Attached to',
                             on_delete=models.CASCADE,
                             related_name='media')
    type = models.SmallIntegerField(choices=MediaType.CHOICES)
    url = models.URLField(blank=False,
                          max_length=2000,
                          validators=[valid_url_media, ])

    def __str__(self):
        return six.text_type(self.pk)

    # Параметры отображения в форме
    widget_labels = dict()
    widget_labels['url'] = 'Url'

    widget_placeholders = defaultdict(lambda: '')
    # Не указанные в словаре поля будут иметь пустую строку placeholder
