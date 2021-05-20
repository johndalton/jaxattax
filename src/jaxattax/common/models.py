import contextlib
import itertools
import typing as t

import wagtail.core.models
from bs4 import BeautifulSoup
from django.apps import apps
from django.utils.translation import gettext_lazy
from wagtail.admin.edit_handlers import (
    CommentPanel, FieldPanel, MultiFieldPanel, PrivacyModalPanel,
    PublishingPanel,
)
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.core.blocks import StreamValue
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailmetadata.models import MetadataPageMixin, WagtailImageMetadataMixin

from jaxattax.utils.breadcrumbs import breadcrumbs_for_page


def strip_tags(html):
    soup = BeautifulSoup(html)
    return soup.get_text()


class WagtailAdminPageForm(WagtailAdminPageForm):
    class Meta:
        labels = {
            'seo_title': "Title",
            'search_description': "Description",
            'search_image': "Image",
        }
        help_texts = {
            'seo_title': "Defaults to the normal page title",
            'search_description': "Defaults to the first Hero Text block in the body",
            'search_image': "Defaults to the first Hero Image in the body, then the site logo",
        }


class Page(MetadataPageMixin, wagtail.core.models.Page):
    base_form_class = WagtailAdminPageForm

    promote_panels = [
        MultiFieldPanel(
            heading=gettext_lazy("Social media settings"),
            help_text=gettext_lazy(
                """
                Set how this page will appear when linked from social media.
                If left blank, each field will use a hopefully sensible default.
                """
            ),
            children=[
                FieldPanel('seo_title'),
                FieldPanel('search_description'),
                ImageChooserPanel('search_image'),
            ],
        ),
    ]
    settings_panels = [
        MultiFieldPanel([
            FieldPanel('slug'),
            FieldPanel('show_in_menus'),
        ], gettext_lazy('Common page configuration')),
        PublishingPanel(),
        PrivacyModalPanel(),
        CommentPanel(),
    ]

    """Base class for all Wagtail Pages in this site"""
    class Meta:
        abstract = True

    def get_breadcrumbs(self, request):
        return breadcrumbs_for_page(self, request)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if 'breadcrumbs' not in context:
            context['breadcrumbs'] = self.get_breadcrumbs(request)
        return context

    def get_meta_image(self):
        if (image := super().get_meta_image()):
            return image

        SiteDecorations = apps.get_model('pages.SiteDecorations')
        site_decorations = SiteDecorations.for_site(self.get_site())
        return site_decorations.logo


class MetadataFromBlocksMixin(WagtailImageMetadataMixin):
    """
    A mixin that fetches some metadata from the content blocks, if it is not
    otherwise set.
    """

    def get_rich_content_blocks(self) -> t.Iterable[StreamValue]:
        """
        Get all the rich_content blocks in the page body. These will be
        used to generate the page social metadata.
        """
        return itertools.chain.from_iterable(
            b.value for b in self.body
            if b.block_type == 'rich_content'
        )

    def get_meta_description(self) -> t.Optional[str]:
        # Try for the search_description, if it has any content
        if (description := super().get_meta_description()):
            return description

        # Otherwise, lets try and get the hero_text content
        with contextlib.suppress(StopIteration):
            hero_text = next(
                block.value
                for block in self.get_rich_content_blocks()
                if block.block_type == 'hero_text'
            )
            return strip_tags(str(hero_text))

        # Alas
        return ""

    def get_meta_image(self):
        # Try for search_image, if it has been set
        if self.search_image:
            return self.search_image

        # Otherwise, lets look for a hero_image
        with contextlib.suppress(StopIteration):
            hero_image = next(
                block.value
                for block in self.get_rich_content_blocks()
                if block.block_type == 'hero_image'
            )
            return hero_image

        # Alas
        return super().get_meta_image()
