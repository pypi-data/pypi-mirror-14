# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals
# Django
from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.utils.translation import ugettext_lazy
# Django REST Framework
from rest_framework import mixins
from rest_framework import generics
# Textbin
from .serializers import TextSerializer
from .models import Text, Media, MediaType
from .forms import TextForm, MediaFormSet, CaptchaForm


class TextCreate(CreateView):
    """ View: create new `Text`-instance with attached `Media` instances
    """
    template_name = "textbin/text_create.html"
    success_url = 'text_detail'
    form_class = TextForm         # Main `Text` instance form
    formset_class = MediaFormSet  # Form of attached `Media` instances
    captcha_form = CaptchaForm    # Form for google reCaptcha2
    max_attach = settings.TEXTBIN['MAX_ATTACH_WEB']  # Limit of attachments

    def is_form_filled(self, form):
        context = self.get_context_data(form=form)
        media_formset = context['media_formset']
        text_form = context['text_form']
        has_text = ('text' in text_form.changed_data)
        has_media = media_formset.has_changed()
        return has_text or has_media

    def get_context_data(self, **kwargs):
        context = super(TextCreate, self).get_context_data(**kwargs)
        context['max_attach'] = self.max_attach
        # context = {}
        if self.request.POST:
            context['text_form'] = self.form_class(self.request.POST)
            context['media_formset'] = self.formset_class(self.request.POST)
            context['text_form'].full_clean()
            context['media_formset'].full_clean()
            context['captcha_form'] = self.captcha_form(self.request.POST)
        else:
            context['text_form'] = self.form_class()
            context['media_formset'] = self.formset_class()
            context['captcha_form'] = self.captcha_form()
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        media_formset = context['media_formset']
        text_form = context['text_form']
        captcha_form = context['captcha_form']
        is_form_filled = self.is_form_filled(form)
        if is_form_filled \
                and (
                     text_form.is_valid() and
                     media_formset.is_valid() and
                     captcha_form.is_valid()
                     ):
            text_form.instance.save()
            new_text = text_form.instance
            for media_form in media_formset.forms:
                url = media_form.instance.url
                if url:
                    Media.objects.create_media(text=new_text, url=url)
            return HttpResponseRedirect(reverse(self.success_url,
                                                args=(text_form.instance.id,)))
        else:
            if not is_form_filled:
                context['error_no_content'] = ugettext_lazy(
                    "You must enter text or add media url(s)")
            return self.render_to_response(context)

    def form_invalid(self, form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        # super(TextCreate, self).post(request, *args, **kwargs)
        self.object = None
        form_class = self.get_form_class()
        formset_class = self.formset_class
        form = self.get_form()
        # Create a formset, form instances with POST data.
        media_formset = formset_class(request.POST, prefix='media')
        text_form = form_class(request.POST)
        # If valid, save the data.
        if media_formset.is_valid() and text_form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class TextDetail(DetailView):
    model = Text
    template_name = "textbin/text_detail.html"
    template_404 = "textbin/text_404.html"

    def get_context_data(self, **kwargs):
        context = super(TextDetail, self).get_context_data(**kwargs)
        text = context['text']
        # use related_name
        context['medias'] = text.media.all()
        # put to context media types
        for mtype in MediaType.CHOICES:
            context[mtype[1].lower()] = mtype[0]
        return context

    def get(self, request, *args, **kwargs):
        # ReImplemented to intercept 404
        try:
            self.object = self.get_object()
        except Http404:
            # return custom template
            return render_to_response(self.template_404, {'request': request},
                                      status=404)
        else:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)


class ApiTextCreate(mixins.CreateModelMixin,
                    generics.GenericAPIView):
    """
    Create a new Text instance
    """
    queryset = Text.objects.all()
    serializer_class = TextSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ApiTextDetail(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):
    """
    Show Text instance details
    """
    queryset = Text.objects.all()
    serializer_class = TextSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
