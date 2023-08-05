# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from django.conf import settings
from django.forms import ModelForm, forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy

from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

from .models import Text, Media


class ModelFormDetail(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelFormDetail, self).__init__(*args, **kwargs)
        # Установка widget-label, widget-placeholder
        for field_name in self.fields:
            placeholder = ugettext_lazy(
                self.Meta.model.widget_placeholders[field_name])
            label = ugettext_lazy(self.Meta.model.widget_labels[field_name])
            self.fields[field_name].widget.attrs['placeholder'] = placeholder
            self.fields[field_name].label = label


class TextForm(ModelFormDetail):
    class Meta:
        model = Text
        fields = ['author_name', 'author_url', 'text']
        # exclude = ['id', 'posted_at']


class MediaInline(ModelFormDetail):
    class Meta:
        model = Media
        fields = ['url']


MediaFormSet = inlineformset_factory(Text,
                                     Media,
                                     form=MediaInline,
                                     extra=1,
                                     can_delete=False,
                                     can_order=False,
                                     max_num=settings.TEXTBIN.get('MAX_ATTACH_WEB', 10))


class CaptchaForm(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())
