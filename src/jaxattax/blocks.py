import dataclasses
import functools

from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock

from . import base_blocks


@functools.total_ordering
@dataclasses.dataclass
class Group:
    name: str
    order: int

    def __lt__(self, other):
        if isinstance(other, str):
            return True
        if not isinstance(other, Group):
            return NotImplemented
        return self.order < other.order

    def deconstruct(self):
        return "jaxattax.blocks.Group", (), dataclasses.asdict(self)

    def __str__(self):
        return self.name


TEXT = Group("Text", 100)
HERO = Group("Big and bold", 200)
IMAGES = Group("Images", 300)
MISC = Group("The kitchen sink", 900)


class LinkBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock()
    document = DocumentChooserBlock()


class RichTextBlocks(blocks.StreamBlock):
    """
    Just rich text, headings, etc.
    """
    heading = blocks.CharBlock(icon='fa-header', group=TEXT)
    subheading = blocks.CharBlock(icon='fa-header', group=TEXT)
    rich_text = blocks.RichTextBlock(
        label="Text",
        features=base_blocks.BLOCK_FEATURES,
        group=TEXT,
    )

    class Meta:
        label = "Rich text content"
        icon = 'fa-align-left'
        template = 'blocks/rich-content.html'


class ButtonBlock(blocks.StructBlock):
    text = blocks.CharBlock()
    link = LinkBlock()


class ButtonsBlock(base_blocks.DeclarativeListBlock):
    child_block = ButtonBlock()

    class Meta:
        label = "A bunch of buttons"
        icon = 'fa-link'
        template = 'blocks/buttons.html'
        group = MISC


class CaptionedImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    alignment = blocks.ChoiceBlock(
        choices=[
            ('full-width', "Full width"),
            ('left', "Left"),
            ('right', "Right"),
        ],
        default="full-width",
    )
    caption = blocks.RichTextBlock(
        help_text="Some short text describing the image",
        features=base_blocks.INLINE_FEATURES,
        required=False,
    )

    class Meta:
        label = "Image with caption"
        help_text = "An image with a short caption"
        icon = 'fa-image'
        template = 'blocks/captioned-image.html'
        group = IMAGES


class SideImageBlock(blocks.StructBlock):
    """Feature image with rich text next to it"""
    image = ImageChooserBlock()
    alignment = blocks.ChoiceBlock([
        ('left', "Left"),
        ('right', "Right"),
    ])
    content = RichTextBlocks()

    class Meta:
        label = "Text next to an image"
        icon = 'fa-address-card'
        template = 'blocks/side-image.html'
        group = IMAGES


class TableOfContentsBlock(blocks.StructBlock):
    class Meta:
        label = "Table of contents"
        help_text = "Displays a table of contents of pages under this page"
        icon = 'fa-list'
        template = 'blocks/table-of-contents.html'
        group = MISC


class CashDonationsBlock(blocks.StructBlock):
    class Meta:
        label = "Cash donations received"
        help_text = "All the cash donations you've received. Real time accountability!"
        icon = 'fa-dollar'
        template = 'blocks/cash-donations.html'
        group = MISC


class RichContentBlocks(RichTextBlocks):
    hero_text = blocks.RichTextBlock(
        label="Hero text",
        help_text="Big and bold, use for important text at the start of a page.",
        features=base_blocks.BLOCK_FEATURES,
        group=HERO,
    )
    hero_image = ImageChooserBlock(
        label="Hero image",
        help_text="Big image, use as the feature image of a page.",
        group=HERO,
    )

    buttons = ButtonsBlock()
    captioned_image = CaptionedImageBlock()
    side_image = SideImageBlock()
    table_of_contents = TableOfContentsBlock()
    cash_donations = CashDonationsBlock()

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


class CallsToActionSection(base_blocks.DeclarativeListBlock):
    child_block = CallToActionBlock()

    class Meta:
        label = "Calls to action"
        icon = 'fa-list-alt'
        template = 'blocks/calls-to-action.html'


class RichContentSection(RichContentBlocks):
    class Meta:
        template = 'blocks/rich-content-section.html'


class PageBlocks(blocks.StreamBlock):
    rich_content = RichContentSection()
    calls_to_action = CallsToActionSection()


class HomePageBlocks(PageBlocks):
    pass
