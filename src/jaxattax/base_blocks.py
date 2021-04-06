import typing as t

from wagtail.core import blocks

# Rich text feature sets
INLINE_FEATURES = ['bold', 'italic', 'link', 'document-link']
BLOCK_FEATURES = INLINE_FEATURES + ['ol', 'ul', 'hr', 'embed']


class DeclarativeListBlock(blocks.ListBlock):
    child_block = None

    def __init__(
        self,
        child_block: t.Union[None, t.Type[blocks.Block], blocks.Block] = None,
        **kwargs,
    ):
        if child_block is None:
            child_block = self.child_block
        super().__init__(child_block, **kwargs)
