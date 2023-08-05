from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError

import coveapi

from stacks_embed.registry import stacks_embed_service_registry
from stacks_embed.utils import retrieve_file_from_url

COVE_API_ID = getattr(settings, 'COVE_API_ID', None)
COVE_API_SECRET = getattr(settings, 'COVE_API_SECRET', None)

if not COVE_API_ID or not COVE_API_SECRET:
    raise ImproperlyConfigured(
        "In order to use the PBS COVE service with stacks_embed you must "
        "define both COVE_API_ID and COVE_API_SECRET in your settings file."
    )

cove_api = coveapi.connect(COVE_API_ID, COVE_API_SECRET)

COVE_EMBED_CODE_TEMPLATE = (
    "<iframe  id='partnerPlayer' frameborder='0' marginwidth='0' "
    "marginheight='0' scrolling='no' width='__WIDTH__' height='__HEIGHT__' "
    "src='http://video.pbs.org/partnerplayer/__EMBEDKEY__/"
    "?autoplay=true&start=0&end=0&chapterbar=true&topbar="
    "false&endscreen=true'></iframe>"
)


def process_cove_video(instance):
    """
    Processes a StacksEmbed instance associated with the COVE service

    Expects that instance.canonical_url is to a valid video on video.pbs.org
    """
    instance.id_on_service = instance.canonical_url.split('/')[-2]
    cove_video = cove_api.videos.filter(
        filter_tp_media_object_id=instance.id_on_service,
        fields='associated_images'
    )
    if cove_video.get('count') == 1:
        results = cove_video.get('results')[0]
        instance.name = results.get('title')
        embed_code_token = results.get('partner_player').strip().split(
            '?')[0].rstrip('/').split('/')[-1]
        print('boo!')
        print(embed_code_token)
        embed_code = COVE_EMBED_CODE_TEMPLATE.replace(
            "__EMBEDKEY__",
            embed_code_token
        )
        print(embed_code)
        instance.embed_code = embed_code
        instance.processed = True
        if not instance.poster_image:
            image_url = None
            for d in results.get('associated_images'):
                if d['type']['eeid'].lower() == 'mezzanine':
                    image_url = d['url']
                    break
            if image_url is not None:
                filename, temp_file = retrieve_file_from_url(image_url)
                temp_file.name = filename
                instance.poster_image = temp_file
    else:
        raise ValidationError(
            '{} is not a URL to a valid COVE video. '
            'Please try again!'.format(instance.canonical_url)
        )

stacks_embed_service_registry.add_embed_service(
    short_name='pbs_cove',
    verbose_name='COVE (PBS Video)',
    allowed_domains=['www.pbs.org'],
    process_instance_func=process_cove_video
)
