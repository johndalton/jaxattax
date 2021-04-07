from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock

from . import base_blocks


class LinkBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock()
    document = DocumentChooserBlock()


class RichTextBlock(blocks.StreamBlock):
    heading = blocks.CharBlock(icon='fa-header')
    subheading = blocks.CharBlock(icon='fa-header')
    rich_text = blocks.RichTextBlock(label="Text", features=base_blocks.BLOCK_FEATURES)

    class Meta:
        label = "Rich text content"
        icon = 'fa-align-left'
        template = 'blocks/rich-content.html'


class SideImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    alignment = blocks.ChoiceBlock([
        ('left', "Left"),
        ('right', "Right"),
    ])
    content = RichTextBlock()

    class Meta:
        label = "Text with side image"
        icon = 'fa-address-card'
        template = 'blocks/side-image.html'


class ButtonBlock(blocks.StructBlock):
    text = blocks.CharBlock()
    link = LinkBlock()


class ButtonsBlock(base_blocks.DeclarativeListBlock):
    child_block = ButtonBlock()

    class Meta:
        label = "A bunch of buttons"
        icon = 'fa-link'
        template = 'blocks/buttons.html'


class LargeImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.RichTextBlock(features=base_blocks.INLINE_FEATURES)

    class Meta:
        label = "Large image"
        icon = 'fa-image'
        template = 'blocks/large-image.html'


class RichContentBlock(RichTextBlock):
    side_image = SideImageBlock()
    buttons = ButtonsBlock()
    large_image = LargeImageBlock()

    class Meta:
        label = "Rich content"
        icon = 'fa-address-card'
        template = 'blocks/rich-content.html'


class CallToActionBlock(blocks.StructBlock):
    heading = blocks.CharBlock()
    image = ImageChooserBlock(blank=True)
    content = blocks.RichTextBlock(features=base_blocks.INLINE_FEATURES)
    link = blocks.PageChooserBlock()
    call_to_action = blocks.CharBlock()

    class Meta:
        label = "Call to action"
        icon = 'fa-list-alt'
        template = 'blocks/call-to-action.html'


class CallsToActionBlock(base_blocks.DeclarativeListBlock):
    child_block = CallToActionBlock()

    class Meta:
        label = "Calls to action"
        icon = 'fa-list-alt'
        template = 'blocks/calls-to-action.html'


class RichContentSection(RichContentBlock):
    class Meta:
        template = 'blocks/rich-content-section.html'


class HomePageBlocks(blocks.StreamBlock):
    rich_content = RichContentSection()
    calls_to_action = CallsToActionBlock()


class PageBlocks(RichContentBlock):
    pass
