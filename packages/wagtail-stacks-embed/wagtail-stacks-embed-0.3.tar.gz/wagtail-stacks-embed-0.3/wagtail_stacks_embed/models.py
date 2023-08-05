from urlparse import urlparse

from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import get_image_model
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet

from .registry import stacks_embed_service_registry

STACKS_EMBED_CHOICES = [
    (key, value[0])
    for key, value in six.iteritems(
        stacks_embed_service_registry._registry
    )
]

models.options.DEFAULT_NAMES = models.options.DEFAULT_NAMES + ('description',)

supported_domains = ', '.join(
    [
        '{}'.format(key)
        for key, value in six.iteritems(
            stacks_embed_service_registry._allowed_domains
        )
    ]
)


@python_2_unicode_compatible
@register_snippet
class StacksEmbed(models.Model, index.Indexed):
    """
    Represents an instance of embeddable media
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
        help_text=_('The internal name/signifier of this content.'),
        blank=True
    )
    poster_image = models.ForeignKey(
        get_image_model(),
        verbose_name=_('Poster Image'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=(
            'NOTE: An image will be automatically generated from the URL.'
        )
    )
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
    canonical_url = models.URLField(
        _('Embed URL'),
        help_text=_(
            'Allowed domains: {}'.format(
                ' '.join([
                    '{}'.format(key)
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
    panels = [
        FieldPanel('canonical_url'),
        MultiFieldPanel(
            [
                FieldPanel('name'),
                ImageChooserPanel('poster_image'),
                FieldPanel('process_on_save'),
            ],
            heading="Metadata Fields",
            classname="collapsible collapsed"
        )
    ]
    search_fields = [
        index.SearchField('name', partial_match=True),
        index.SearchField('service', partial_match=True),
    ]

    def __str__(self):
        return u"{} | {}".format(self.name, self.get_service_display())

    class Meta:
        verbose_name = _('Embeddable Media')
        verbose_name_plural = _('Embeddable Media')
        ordering = ('-date_created', '-date_modified')
        description = 'Supported domains: {}'.format(supported_domains)

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
