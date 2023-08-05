from urlparse import urlparse

from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from textplusstuff.fields import TextPlusStuffField
from versatileimagefield.fields import VersatileImageField, PPOIField

from .registry import stacks_embed_service_registry

STACKS_EMBED_CHOICES = [
    (key, value[0])
    for key, value in six.iteritems(
        stacks_embed_service_registry._registry
    )
]


class StacksEmbedBase(models.Model):
    """
    An abstract base model that keeps track of when a model instance
    was created and last-updated.
    """
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    date_modified = models.DateTimeField(
        auto_now=True
    )
    name = models.CharField(
        _('Name'),
        max_length=100,
        help_text=_('The internal name/signifier of this content.')
    )
    display_title = models.CharField(
        _('Display Title'),
        max_length=100,
        help_text=_(
            'An optional displayed-to-the-user title of this content.'
        ),
        blank=True
    )

    class Meta:
        abstract = True


@python_2_unicode_compatible
class StacksEmbed(StacksEmbedBase):
    """
    Represents an instance of embeddable media
    """
    overline = models.CharField(
        _('Overline'),
        max_length=100,
        help_text=_(
            'An optional displayed-to-the-user overline of this content. '
            'Overlines are typically included above the Display Title.'
        ),
        blank=True
    )
    poster_image = VersatileImageField(
        _('Poster Image'),
        upload_to='stacks_embed/poster_image',
        ppoi_field='poster_image_ppoi',
        blank=True,
        null=True
    )
    poster_image_ppoi = PPOIField()
    service = models.CharField(
        _('Service'),
        choices=STACKS_EMBED_CHOICES,
        max_length=30,
        help_text="The service you want to embed from."
    )
    id_on_service = models.CharField(
        _('Service ID'),
        max_length=120,
        help_text="The ID of the content on the service."
    )
    embed_code = models.TextField(
        _('Embed Code')
    )
    optional_content = TextPlusStuffField(
        _('Optional Accompanying Content'),
        blank=True,
        help_text=_(
            "A field to enter optional accompanying content. Example uses: "
            "captions, credits or accompanying content."
        )
    )
    canonical_url = models.URLField(
        _('Canonical URL'),
        help_text=_(
            'The originating URL of this embeddable content. Allowed '
            'domains: {}'.format(
                ''.join([
                    '<p class="help">- {}</p>'.format(key)
                    for key, value in six.iteritems(
                        stacks_embed_service_registry._allowed_domains
                    )
                ])
            )
        )
    )
    process_on_save = models.BooleanField(
        _('Process on Save?'),
        default=True,
        help_text=(
            'A boolean (True/False) signifying if this instance should be '
            'processed by its associated API on save.'
        )
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Stacks Embed')
        verbose_name_plural = _('Stacks Embeds')

    def clean_canonical_url(self):
        """
        Ensures `canonical_url` is associated with a domain registered with
        the Stacks Embed Service Registry
        """
        data = self.cleaned_data['canonical_url']
        canonical_url_parsed = urlparse(data)
        if (
            canonical_url_parsed.netloc
        ) not in stacks_embed_service_registry._allowed_domains:
            raise ValidationError(
                "{} is not an allowed. Only URLS from the following "
                "domains can be used: {}".format(
                    data,
                    ", ".join([
                        key
                        for key, value in six.iteritems(
                            stacks_embed_service_registry._allowed_domains
                        )
                    ])
                )
            )
        return data

    def clean(self):
        canonical_url_parsed = urlparse(self.canonical_url)
        if (
            canonical_url_parsed.netloc
        ) not in stacks_embed_service_registry._allowed_domains:
            raise ValidationError(
                "{} is a URL from an unallowed domain. Only URLS from the "
                "following domains can be used: {}".format(
                    self.canonical_url,
                    ", ".join([
                        key
                        for key, value in six.iteritems(
                            stacks_embed_service_registry._allowed_domains
                        )
                    ])
                )
            )
        else:
            self.service = stacks_embed_service_registry.\
                _allowed_domains.get(canonical_url_parsed.netloc)
            if self.process_on_save is True:
                stacks_embed_service_registry._registry[
                    self.service
                ][1](self)
                self.process_on_save = False


@python_2_unicode_compatible
class StacksEmbedList(StacksEmbedBase):
    """Represents a list of StacksEmbed instances."""

    embeds = models.ManyToManyField(
        StacksEmbed,
        through='StacksEmbedListEmbed'
    )

    class Meta:
        verbose_name = _('Stacks Embed List')
        verbose_name_plural = _('Stacks Embed Lists')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class StacksEmbedListEmbed(models.Model):
    """
    A through table for connecting StacksEmbed instances to StacksEmbedList
    instances.
    """
    embed_list = models.ForeignKey(
        StacksEmbedList
    )
    order = models.PositiveIntegerField()
    embed = models.ForeignKey(
        StacksEmbed
    )

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return "{} {}. {}".format(
            self.embed_list.name,
            self.order,
            self.embed.name,
        )


@receiver(models.signals.pre_save, sender=StacksEmbed)
def process_service(sender, instance, **kwargs):
    """
    Ensures StacksEmbed.full_clean() is ALWAYS called.
    """
    try:
        instance.full_clean()
    except ValidationError as e:
        # Do something based on the errors contained in e.message_dict.
        # Display them to a user, or handle them programmatically.
        pass
        del e
