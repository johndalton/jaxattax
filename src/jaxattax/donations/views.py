from django import http

from jaxattax.utils.breadcrumbs import Crumb

from . import forms, models


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
