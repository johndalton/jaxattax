from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtailnews.decorators import newsindex
from wagtailnews.models import (AbstractNewsItem, AbstractNewsItemRevision,
                                NewsIndexMixin)

from .. import blocks


@newsindex
class NewsIndex(NewsIndexMixin, Page):
    newsitem_model = 'NewsItem'
    parent_page_types = ['pages.HomePage']

    template = 'layouts/news/news_index.html'


class NewsItem(AbstractNewsItem):
    title = models.CharField(max_length=100)
    body = StreamField(blocks.RichContentBlocks())

    panels = [
        FieldPanel('title'),
        StreamFieldPanel('body'),
    ]

    template = 'layouts/news/news_item.html'

    def __str__(self):
        return self.title


# This table is used to store revisions of the news items.
class NewsItemRevision(AbstractNewsItemRevision):
    # This is the only field you need to define on this model.
    # It must be a foreign key to your NewsItem model,
    # be named 'newsitem', and have a related_name='revisions'
    newsitem = models.ForeignKey(NewsItem, related_name='revisions', on_delete=models.CASCADE)
