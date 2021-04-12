import typing as t

from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.fields import ImageField

from jaxattax.mixins import PageWithBreadcrumbs

from .. import blocks


class HomePage(Page):
    body = StreamField(blocks.HomePageBlocks())

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    template = 'layouts/pages/home.html'

    parent_page_types = ['wagtailcore.Page']


class Page(PageWithBreadcrumbs):
    body = StreamField(blocks.PageBlocks())
    show_table_of_contents = models.BooleanField(default=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
    settings_panels = Page.settings_panels + [
        FieldPanel('show_table_of_contents'),
    ]

    template = 'layouts/pages/page.html'

    parent_page_types = ['pages.HomePage', 'Page']



@register_setting(icon="link")
class ContactDetails(BaseSetting):
    email = models.EmailField(blank=True)
    twitter_handle = models.CharField(blank=True, max_length=30)
    instagram_handle = models.CharField(blank=True, max_length=30)
    facebook_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)

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
