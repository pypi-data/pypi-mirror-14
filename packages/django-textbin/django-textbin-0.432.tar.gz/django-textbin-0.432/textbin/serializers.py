# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals
from django.utils.translation import ugettext as _
from rest_framework import serializers
from .models import Text, Media


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text

    # Attached medias urls
    media = serializers.ListField(
        child=serializers.URLField(required=True),
        required=False)

    # Set types of attachment media.
    # No child - no validation: allowed integers or text.
    types = serializers.ListField(required=False)

    def create(self, validated_data):
        """
        Create a new `Text` instance and it`s attached 'Media'
        instances, given the validated data, return new 'Text' instance
        """
        # Get media's urls
        urls = validated_data.pop('media', [])
        # and types
        types = validated_data.pop('types', [])
        if len(types) != len(urls):
            # incompatible lenghts,
            # we will use type-autodetection instead obtained types
            types = ['']*len(urls)

        # Create Text instance
        new_text = Text(**validated_data)

        # Additional check: user must input text or add media url(s)
        if not (urls or new_text.text):
            raise serializers.ValidationError(
                _("You must enter text or add media url(s)"))
        else:
            new_text.save()

        # Create Media instances
        for url, type_ in zip(urls, types):
            if url and type:
                Media.objects.create_media(url=url, text=new_text, type_=type_)
            elif url:
                Media.objects.create_media(url=url, text=new_text)

        return new_text

    def to_representation(self, obj):
        """ Return details for `Text` instance and it`s attached `Media`
        """
        # Add Text data
        text = {'id':          obj.id,
                'author_name': obj.author_name,
                'author_url':  obj.author_url,
                'posted_at':   obj.posted_at,
                'text':        obj.text}
        # Create attached media's urls list
        urls = list()
        types = list()
        medias = obj.media.all()
        for media in medias:
            urls.append(media.url)
            types.append(media.type)
        text['media'] = urls
        text['types'] = types
        return text
