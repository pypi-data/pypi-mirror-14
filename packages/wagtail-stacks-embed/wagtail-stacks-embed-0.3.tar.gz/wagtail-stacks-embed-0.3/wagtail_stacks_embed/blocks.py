from copy import deepcopy

from wagtail.wagtailcore.blocks import (
    TextBlock,
    RichTextBlock
)
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock

from streamfield_tools.blocks import (
    Rendition,
    RenditionAwareListBlock,
    MultiRenditionStructBlock,
    RenditionAwareStructBlock
)

from .models import StacksEmbed

stacks_embed_form_blocks = [
    ('embed', SnippetChooserBlock(StacksEmbed)),
    ('overline', TextBlock(required=False)),
    ('title', TextBlock(required=False)),
    ('additional_content', RichTextBlock(required=False))
]

stacks_embed_block = MultiRenditionStructBlock(
    deepcopy(stacks_embed_form_blocks),
    core_renditions=(
        Rendition(
            short_name='full_width',
            verbose_name='Full Width Embed',
            description="An embed that spans the full width of it's "
                        "containing div.",
            path_to_template='wagtail_stacks_embed/single/full_width.html',
            image_rendition='fill-1600x901'
        ),
        Rendition(
            short_name='embed_left_content_right',
            verbose_name='Embed Left, Content Right',
            description="Display an embed on the left with it's "
                        "accompanying content on the right.",
            path_to_template='wagtail_stacks_embed/single/'
                             'embed_left_content_right.html',
            image_rendition='fill-800x450'
        ),
        Rendition(
            short_name='embed_right_content_left',
            verbose_name='Embed Right, Content Left',
            description="Display an embed on the right with it's accompanying "
                        "content on the left.",
            path_to_template='wagtail_stacks_embed/single/'
                             'embed_right_content_left.html',
            image_rendition='fill-800x450'
        )
    ),
    addl_renditions_settings_key='stacks_embed_block',
    label='Media Embed',
    icon='snippet'
)


stacks_embedlist_block = MultiRenditionStructBlock(
    [
        ('title', TextBlock(required=False)),
        ('embeds', RenditionAwareListBlock(
            RenditionAwareStructBlock(
                deepcopy(stacks_embed_form_blocks),
                template='wagtail_stacks_embed/list/list-item.html',
                template_carousel='wagtail_stacks_embed/list/'
                                  'list-item-carousel.html'
            )
        ))
    ],
    core_renditions=(
        Rendition(
            short_name='1up',
            verbose_name="Embed List 1-Up",
            description="A list of embeds displayed in grid with one image "
                        "in each row.",
            path_to_template='wagtail_stacks_embed/list/1up.html',
            image_rendition='fill-1600x901'
        ),
        Rendition(
            short_name='2up',
            verbose_name="Embed List 2-Up",
            description="A list of embeds displayed in grid with two "
                        "in each row.",
            path_to_template='wagtail_stacks_embed/list/2up.html',
            image_rendition='fill-800x450'
        ),
        Rendition(
            short_name='3up',
            verbose_name="Embed List 3-Up",
            description="A list of embeds displayed in grid with three "
                        "in each row.",
            path_to_template='wagtail_stacks_embed/list/3up.html',
            image_rendition='fill-700x390'
        ),
        Rendition(
            short_name='carousel',
            verbose_name="Embed Carousel / Gallery",
            description="A list of embeds displayed in a javascript-powered "
                        "carousel.",
            path_to_template='wagtail_stacks_embed/list/carousel.html',
            image_rendition='fill-1600x901'
        )
    ),
    addl_renditions_settings_key='stacks_embedlist_block',
    label='Media Embed List',
    icon='snippet'
)
