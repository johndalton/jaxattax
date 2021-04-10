from wagtail.core import blocks

from jaxattax.blocks import RichContentBlocks


class DonateBlock(blocks.StructBlock):
    class Meta:
        label = "Donate"
        help_text = "Get that dolla dolla billz"
        icon = 'fa-dollar'
        template = 'blocks/donations/donate.html'


class DonateBlocks(RichContentBlocks):
    donate = DonateBlock()


class SuccessBlocks(RichContentBlocks):
    pass
