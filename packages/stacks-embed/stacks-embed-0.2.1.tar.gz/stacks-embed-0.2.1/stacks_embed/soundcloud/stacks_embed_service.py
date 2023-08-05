from django.core.exceptions import ValidationError

import requests
from bs4 import BeautifulSoup

from stacks_embed.registry import stacks_embed_service_registry
from stacks_embed.utils import retrieve_file_from_url


def process_soundcloud_url(instance):
    """
    Processes a StacksEmbed instance associated with the YouTube service

    Expects that instance.canonical_url is to a valid video on either
    www.youtube.com or youtu.be
    """
    sc_page = requests.get(instance.canonical_url)

    if sc_page.status_code == 200:
        sc_page_parsed = BeautifulSoup(sc_page.content)
        instance.id_on_service = sc_page_parsed.find(
            property="al:ios:url"
        )['content'].split(':')[-1]
        instance.name = sc_page_parsed.find(property="og:title")['content']
        image_url = sc_page_parsed.find(
            property="og:image"
        )['content'].replace('https', 'http')
        if image_url and not instance.poster_image:
            filename, temp_file = retrieve_file_from_url(image_url)
            temp_file.name = filename
            instance.poster_image = temp_file
        instance.embed_code = (
            '<iframe width="100%" height="450" scrolling="no" '
            'frameborder="no" src="https://w.soundcloud.com/player/?url='
            'https%3A//api.soundcloud.com/tracks/{}&amp;auto_play=false&amp;'
            'hide_related=false&amp;show_comments=true&amp;show_user=true&amp;'
            'show_reposts=false&amp;visual=true"></iframe>'
        ).format(instance.id_on_service)
    else:
        if sc_page.status_code == 404:
            error_msg = (
                '{} is an unavailable URL on SoundCloud. '
                'Double-check it and try again!'
            )
        else:
            error_msg = (
                'There was an error processing {}. Please try again later!'
            )
        raise ValidationError(error_msg.format(instance.canonical_url))

stacks_embed_service_registry.add_embed_service(
    short_name='soundcloud',
    verbose_name='SoundCloud',
    allowed_domains=['soundcloud.com'],
    process_instance_func=process_soundcloud_url
)
