from textplusstuff import registry

from .models import StacksEmbed, StacksEmbedList
from .serializers import StacksEmbedSerializer, StacksEmbedListSerializer


class StacksEmbedStuff(registry.ModelStuff):
    # The queryset used to retrieve instances of TestModel
    # within the front-end interface. For instance, you could
    # exclude 'unpublished' instances or anything else you can
    # query the ORM against
    queryset = StacksEmbed.objects.exclude(
        embed_code='',
        name=''
    )

    description = 'A single embed with optional content.'

    # The serializer we just defined, this is what provides the context/JSON
    # payload for this Stuff
    serializer_class = StacksEmbedSerializer

    # All Stuff must have at least one rendition (specified in
    # the `renditions` attribute below) which basically
    # just points to a template and some human-readable metadata.
    # At present there are only two options for setting rendition_type:
    # either 'block' (the default) or inline. These will be used by
    # the front-end editor when placing tokens.
    renditions = [
        registry.Rendition(
            short_name='full_width',
            verbose_name="Full Width Embed",
            description="An embed that spans the full width of it's "
                        "containing div.",
            path_to_template='stacks_embed/stacksembed/'
                             'stacksembed-full_width.html'
        ),
        registry.Rendition(
            short_name='embed_left_content_right',
            verbose_name="Embed Left, Content Right",
            description="Display an embed on the left with it's accompanying "
                        "content on the right. NOTE: This rendition should "
                        "only be used if the 'Optional Content' field is "
                        "filled out.",
            path_to_template='stacks_embed/stacksembed/'
                             'stacksembed-embed_left_content_right.html'
        ),
        registry.Rendition(
            short_name='embed_right_content_left',
            verbose_name="Embed Right, Content Left",
            description="Display an embed on the right with it's accompanying "
                        "content on the left. NOTE: This rendition should "
                        "only be used if the 'Optional Content' field is "
                        "filled out.",
            path_to_template='stacks_embed/stacksembed/'
                             'stacksembed-embed_right_content_left.html'
        )
    ]
    # The attributes used in the list (table) display of the front-end
    # editing tool.
    list_display = ('id', 'name')


class StacksEmbedListStuff(registry.ModelStuff):
    # The queryset used to retrieve instances of TestModel
    # within the front-end interface. For instance, you could
    # exclude 'unpublished' instances or anything else you can
    # query the ORM against
    queryset = StacksEmbedList.objects.prefetch_related(
        'stacksembedlistembed_set',
        'stacksembedlistembed_set__embed'
    )

    description = 'A list of embeds with optional content.'
    serializer_class = StacksEmbedListSerializer

    # All Stuff must have at least one rendition (specified in
    # the `renditions` attribute below) which basically
    # just points to a template and some human-readable metadata.
    # At present there are only two options for setting rendition_type:
    # either 'block' (the default) or inline. These will be used by
    # the front-end editor when placing tokens.
    renditions = [
        registry.Rendition(
            short_name='1up',
            verbose_name="Embed List 1-Up",
            description="A list of embeds displayed in grid with one image "
                        "in each row.",
            path_to_template='stacks_embed/stacksembedlist/'
                             'stacksembedlist-1up.html'
        ),
        registry.Rendition(
            short_name='2up',
            verbose_name="Embed List 2-Up",
            description="A list of embeds displayed in grid with two "
                        "in each row.",
            path_to_template='stacks_embed/stacksembedlist/'
                             'stacksembedlist-2up.html'
        ),
        registry.Rendition(
            short_name='3up',
            verbose_name="Embed List 3-Up",
            description="A list of embeds displayed in grid with three "
                        "in each row.",
            path_to_template='stacks_embed/stacksembedlist/'
                             'stacksembedlist-3up.html'
        ),
        registry.Rendition(
            short_name='gallery',
            verbose_name="Embed Gallery",
            description="A list of embeds displayed in a javascript-powered "
                        "gallery/carousel.",
            path_to_template='stacks_embed/stacksembedlist/'
                             'stacksembedlist-gallery.html'
        )
    ]
    # The attributes used in the list (table) display of the front-end
    # editing tool.
    list_display = ('id', 'list_name')

registry.stuff_registry.add_modelstuff(
    StacksEmbed,
    StacksEmbedStuff,
    groups=['stacks', 'media']
)

registry.stuff_registry.add_modelstuff(
    StacksEmbedList,
    StacksEmbedListStuff,
    groups=['stacks', 'media']
)
