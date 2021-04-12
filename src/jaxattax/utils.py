import dataclasses

from django import http
from django.core.paginator import EmptyPage, Paginator
from wagtail.core.models import Page, Site


def paginate(request, items):
    paginator = Paginator(items, 5)

    try:
        page_number = int(request.GET['page'])
        page = paginator.page(page_number)
    except (ValueError, KeyError, EmptyPage):
        page = paginator.page(1)

    return paginator, page


@dataclasses.dataclass
class Crumb:
    title: str
    url: str


def breadcrumbs_for_page(page: Page, request: http.HttpRequest):
    site = Site.find_for_request(request)
    ancestors = page.get_ancestors(inclusive=True).descendant_of(site.root_page, inclusive=True).live().specific()
    return [Crumb(title=p.title, url=p.get_url(request=request)) for p in ancestors]
