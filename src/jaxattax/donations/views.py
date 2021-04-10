import logging
from decimal import Decimal

import stripe
from django import http, views
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic.edit import FormMixin

from jaxattax.utils.breadcrumbs import Crumb

from . import forms, models

logger = logging.getLogger(__name__)


def donate_index(request: http.HttpRequest, page: models.DonatePage):
    return page.render(
        request,
        context_overrides={
            'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
            'donate_form': forms.DonateForm(initial={'page': page}),
        }
    )


def donate_success(request, page):
    breadcrumbs = page.get_breadcrumbs(request) + [
        Crumb(title="Thanks", url=request.path)
    ]
    return page.render(
        request, template=page.thanks_template,
        context_overrides={
            'breadcrumbs': breadcrumbs,
        },
    )


class CreateSession(FormMixin, views.View):
    form_class = forms.DonateForm

    def post(self, request):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        page = form.cleaned_data['page']
        page_url = page.get_full_url()

        dollars = form.cleaned_data['amount']

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'aud',
                        'unit_amount': dollars * 100,
                        'product_data': {
                            'name': "Donation",
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={'name': form.data['name']},
            mode='payment',
            success_url=page_url + page.reverse_subpage('success'),
            cancel_url=page_url,
        )
        return http.JsonResponse({
            'id': checkout_session.id
        })

    def form_invalid(self, form):
        print(form.errors)
        return http.JsonResponse({
            'errors': ['YOu done fucked up'],
        })


@csrf_exempt
@require_POST
def receive_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )

    except (ValueError, stripe.error.SignatureVerificationError) as e:
        print(e)
        return http.HttpResponse(status=400)

    logger.info(f"Got stripe webhook {event['type']!r}")

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        name = session["metadata"].get('name', 'Unknown')

        dollars = Decimal(session['amount_total']) / 100
        models.CashDonation.objects.create(
            name=name,
            amount=dollars,
            date=timezone.now().date(),
            stripe_id=session['payment_intent'],
        )

        # TODO - send an email to the customer

    return http.HttpResponse(status=200)
