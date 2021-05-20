import typing as t

from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images.edit_handlers import ImageChooserPanel

from jaxattax.common.models import MetadataFromBlocksMixin, Page, StreamField

from . import blocks


class HomePage(Page):
    body = StreamField(blocks.HomePageBlocks())

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    template = 'layouts/pages/home.html'

    parent_page_types = ['wagtailcore.Page']


class Page(MetadataFromBlocksMixin, Page):
    body = StreamField(blocks.PageBlocks())

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    template = 'layouts/pages/page.html'

    show_in_menus_default = True
    parent_page_types = ['pages.HomePage', 'Page']


@register_setting(icon="link")
class ContactDetails(BaseSetting):
    email = models.EmailField(blank=True)
    twitter_handle = models.CharField(blank=True, max_length=30)
    instagram_handle = models.CharField(blank=True, max_length=30)
    facebook_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)

    name = models.CharField(
        max_length=200,
        help_text="Your name, used on invoices and other such things."
    )
    abn = models.CharField(
        max_length=15,
        help_text="The ABN put on invoices and the like",
    )

    @property
    def twitter_url(self) -> t.Optional[str]:
        if not self.twitter_handle:
            return None
        return 'https://twitter.com/' + self.twitter_handle

    @property
    def instagram_url(self) -> t.Optional[str]:
        if not self.instagram_handle:
            return None
        return 'https://instagram.com/' + self.instagram_handle


@register_setting(icon='fa-star-o')
class SiteDecorations(BaseSetting):
    site_name = models.CharField(max_length=200)
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    authorized_by = models.CharField(max_length=255)

    panels = [
        ImageChooserPanel('logo'),
        FieldPanel('site_name'),
        FieldPanel('authorized_by'),
    ]
