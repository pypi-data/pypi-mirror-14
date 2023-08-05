from django.core.exceptions import ValidationError

import requests
from bs4 import BeautifulSoup

from stacks_embed.registry import stacks_embed_service_registry
from stacks_embed.utils import retrieve_file_from_url


def process_vimeo_url(instance):
    """
    Processes a StacksEmbed instance associated with Vimeo

    Expects that instance.canonical_url is to a valid video on either
    www.youtube.com or youtu.be
    """
    vimeo_page = requests.get(instance.canonical_url)

    if vimeo_page.status_code == 200:
        vimeo_page_parsed = BeautifulSoup(vimeo_page.content)
        instance.canonical_url = vimeo_page_parsed.find(
            property="og:url"
        )['content']
        instance.id_on_service = instance.canonical_url.split('/')[-1]
        instance.name = vimeo_page_parsed.find(property="og:title")['content']
        image_url = vimeo_page_parsed.find(
            property="og:image"
        )['content'].replace('https', 'http')
        if image_url and not instance.poster_image:
            filename, temp_file = retrieve_file_from_url(image_url)
            temp_file.name = "{}-{}.jpg".format(
                filename, instance.id_on_service
            )
            instance.poster_image = temp_file
        instance.embed_code = (
            '<iframe src="//player.vimeo.com/video/{}" width="500" '
            'height="281" frameborder="0" webkitallowfullscreen '
            'mozallowfullscreen allowfullscreen></iframe>'
        ).format(instance.id_on_service)
    else:
        if vimeo_page.status_code == 404:
            error_msg = (
                '{} is an unavailable URL on Vimeo. '
                'Double-check it and try again!'
            )
        else:
            error_msg = (
                'There was an error processing {}. Please try again later!'
            )
        raise ValidationError(error_msg.format(instance.canonical_url))

stacks_embed_service_registry.add_embed_service(
    short_name='vimeo',
    verbose_name='Vimeo',
    allowed_domains=['vimeo.com'],
    process_instance_func=process_vimeo_url
)
