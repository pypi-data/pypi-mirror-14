from streamfield_tools.registry import block_registry

from .blocks import (
    stacks_embed_block,
    stacks_embedlist_block
)

block_registry.register_block(
    'embed',
    stacks_embed_block
)

block_registry.register_block(
    'embed_list',
    stacks_embedlist_block
)
