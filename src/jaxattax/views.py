from django.http import Http404
from django.shortcuts import redirect, render
from wagtail.core.models import Site

from jaxattax.pages.models import SiteDecorations


def favicon(request):
    try:
        site = Site.find_for_request(request)
        site_decorations = SiteDecorations.for_site(site)
    except (Site.DoesNotExist, SiteDecorations.DoesNotExist):
        raise Http404()

    if site_decorations.logo is None:
        raise Http404()

    rendition = site_decorations.logo.get_rendition('max-72x72|format-png')
    return redirect(rendition.url)


def handler404(request, *args, **kwargs):
    return render(request, "layouts/404.html", status=404)


def handler500(request, *args, **kwargs):
    return render(request, "layouts/500.html", status=500)
