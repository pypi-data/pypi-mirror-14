from __future__ import unicode_literals

from django.conf import settings

from rest_framework import serializers
from textplusstuff.serializers import (
    ExtraContextSerializerMixIn,
    TextPlusStuffFieldSerializer
)
from versatileimagefield.serializers import VersatileImageFieldSerializer

from .models import StacksEmbed, StacksEmbedList

image_sets = getattr(
    settings,
    'VERSATILEIMAGEFIELD_RENDITION_KEY_SETS',
    {}
).get(
    'stacks_embed_poster_image',
    [
        ('full_size', 'url'),
        ('gallery_thumb', 'crop__400x225'),
        ('3up_thumb', 'crop__700x394'),
        ('2up_thumb', 'crop__800x450'),
        ('full_width', 'crop__1600x901'),
    ]
)


class StacksEmbedSerializer(ExtraContextSerializerMixIn,
                            serializers.ModelSerializer):
    """Serializes StacksImage instances"""
    poster_image = VersatileImageFieldSerializer(
        sizes=image_sets
    )
    optional_content = TextPlusStuffFieldSerializer()

    class Meta:
        model = StacksEmbed
        fields = (
            'name',
            'overline',
            'display_title',
            'poster_image',
            'service',
            'id_on_service',
            'embed_code',
            'optional_content',
            'canonical_url'
        )


class StacksEmbedListSerializer(ExtraContextSerializerMixIn,
                                serializers.ModelSerializer):
    embeds = serializers.SerializerMethodField()

    class Meta:
        model = StacksEmbedList
        fields = ('name', 'display_title', 'embeds')

    def get_embeds(self, obj):
        """Order `embeds` field properly."""
        embeds = obj.embeds.order_by('stacksembedlistembed__order')
        embeds = StacksEmbedSerializer(embeds, many=True)
        return embeds.data
