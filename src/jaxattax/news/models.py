from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtailnews.decorators import newsindex
from wagtailnews.models import (
    AbstractNewsItem,
    AbstractNewsItemRevision,
    NewsIndexMixin
)

from jaxattax.mixins import PageWithBreadcrumbs
from jaxattax.utils.breadcrumbs import Crumb

from . import blocks


@newsindex
class NewsIndex(NewsIndexMixin, PageWithBreadcrumbs):
    newsitem_model = 'NewsItem'
    show_in_menus_default = True
    parent_page_types = ['pages.HomePage']

    template = 'layouts/news/news_index.html'


class NewsItem(AbstractNewsItem):
    title = models.CharField(max_length=100)
    body = StreamField(blocks.NewsItemBlocks())

    panels = [
        FieldPanel('title'),
        StreamFieldPanel('body'),
    ]

    template = 'layouts/news/news_item.html'

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['breadcrumbs'].append(Crumb(title=self.title, url=self.url))
        return context

    def __str__(self):
        return self.title


# This table is used to store revisions of the news items.
class NewsItemRevision(AbstractNewsItemRevision):
    # This is the only field you need to define on this model.
    # It must be a foreign key to your NewsItem model,
    # be named 'newsitem', and have a related_name='revisions'
    newsitem = models.ForeignKey(NewsItem, related_name='revisions', on_delete=models.CASCADE)
