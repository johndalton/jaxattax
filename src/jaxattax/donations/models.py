from django.db import models
from wagtail.admin.edit_handlers import (
    FieldPanel, ObjectList, StreamFieldPanel, TabbedInterface,
)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import StreamField

from jaxattax.common.models import MetadataFromBlocksMixin, Page
from jaxattax.edit_handlers import ReadOnlyPanel
from jaxattax.utils.view_proxy import ViewModuleProxy

from . import blocks

views = ViewModuleProxy('jaxattax.donations.views')


class DonatePage(MetadataFromBlocksMixin, RoutablePageMixin, Page):
    body = StreamField(blocks.DonateBlocks)
    success_body = StreamField(blocks.SuccessBlocks)

    donate_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
    thanks_panels = [
        StreamFieldPanel(
            'success_body',
            heading="Thanks message",
            help_text="This page will be shown to people after they have donated",
        ),
    ]

    edit_handler = TabbedInterface([
        ObjectList(donate_panels, heading="Donate"),
        ObjectList(thanks_panels, heading="Thanks"),
        ObjectList(Page.promote_panels, heading="Promote"),
        ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
    ])

    template = 'layouts/donations/donate.html'
    thanks_template = 'layouts/donations/thanks.html'

    show_in_menus_default = True
    parent_page_types = ['pages.HomePage', 'pages.Page']

    _v_index = route('^$', 'index')(views['donate_index'])
    _v_success = route('^thanks/$', 'success')(views['donate_success'])


class CashDonation(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    created = models.DateTimeField(auto_now_add=True)

    email = models.EmailField(
        blank=True,
        help_text=(
            "The email address entered in the Stripe payment. "
            "Not required for manually entered donations."
        ),
    )
    receipt_sent = models.BooleanField(
        default=False,
        help_text="Has an automatic receipt been emailed?",
    )
    stripe_id = models.CharField(
        max_length=100, blank=True,
        help_text="The ID of the payment in Stripe, if it was done online.",
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('amount'),
        FieldPanel('date'),
        FieldPanel('email'),
        ReadOnlyPanel('stripe_id', heading="Stripe transaction ID"),
    ]

    def __str__(self):
        return f"Donation from {self.name} on {self.date} for ${self.amount:.2f}"

    class Meta:
        ordering = ['-date', '-created']
