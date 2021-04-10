import dataclasses

from django import http
from wagtail.core.models import Page, Site


@dataclasses.dataclass
class Crumb:
    title: str
    url: str


def breadcrumbs_for_page(page: Page, request: http.HttpRequest):
    site = Site.find_for_request(request)
    ancestors = page.get_ancestors(inclusive=True).descendant_of(site.root_page, inclusive=True).live().specific()
    return [Crumb(title=p.title, url=p.get_url(request=request)) for p in ancestors]
