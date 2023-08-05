from django.core.exceptions import ValidationError

import requests
from bs4 import BeautifulSoup

from stacks_embed.registry import stacks_embed_service_registry
from stacks_embed.utils import retrieve_file_from_url


def process_youtube_video(instance):
    """
    Processes a StacksEmbed instance associated with the YouTube service

    Expects that instance.canonical_url is to a valid video on either
    www.youtube.com or youtu.be
    """
    youtube_page = requests.get(instance.canonical_url)

    if youtube_page.status_code == 200:
        youtube_parsed = BeautifulSoup(youtube_page.content)
        try:
            official_url = youtube_parsed.find(property="og:url")['content']
        except TypeError:
            raise ValidationError(
                '{} is an unavailable URL on YouTube. '
                'Double-check it and try again!'.format(instance.canonical_url)
            )
        else:
            instance.id_on_service = official_url.split('=')[-1]
            instance.name = youtube_parsed.find(property="og:title")['content']
            image_url = youtube_parsed.find(property="og:image")['content']
            if image_url and not instance.poster_image:
                filename, temp_file = retrieve_file_from_url(image_url)
                filename = '{}-{}'.format(instance.id_on_service, filename)
                temp_file.name = filename
                instance.poster_image = temp_file
            instance.embed_code = (
                '<iframe width="__WIDTH__" height="__HEIGHT__" '
                'src="https://www.youtube.com/'
                'embed/{}" frameborder="0" allowfullscreen></iframe>'
            ).format(instance.id_on_service)

stacks_embed_service_registry.add_embed_service(
    short_name='youtube',
    verbose_name='YouTube',
    allowed_domains=[
        'www.youtube.com',
        'youtu.be'
    ],
    process_instance_func=process_youtube_video
)
