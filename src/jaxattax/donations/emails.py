from email.headerregistry import Address

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from jaxattax.pages.models import ContactDetails

from . import models


def _make_receipt(
    cash_donation: models.CashDonation,
    contact_details: ContactDetails
) -> EmailMultiAlternatives:
    subject = f"Tax invoice #{cash_donation.id} for donation to {contact_details.name}"
    from_email = Address(display_name=contact_details.name, addr_spec=settings.DEFAULT_FROM_EMAIL)
    reply_to_email = Address(display_name=contact_details.name, addr_spec=contact_details.email)
    to_email = Address(display_name=cash_donation.name, addr_spec=cash_donation.email)

    context = {
        'from_name': contact_details.name,
        'from_abn': contact_details.abn,
        'to_name': cash_donation.name,
        'amount': cash_donation.amount,
        'date': cash_donation.date,
    }
    text_body = render_to_string('emails/donations/receipt.txt', context=context)
    html_body = render_to_string('emails/donations/receipt.html', context=context)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=[to_email],
        reply_to=[reply_to_email],
    )
    email.attach_alternative(html_body, 'text/html')
    return email


def send_receipt(
    cash_donation: models.CashDonation,
    contact_details: ContactDetails
) -> None:
    email = _make_receipt(
        cash_donation=cash_donation,
        contact_details=contact_details,
    )
    email.send()
