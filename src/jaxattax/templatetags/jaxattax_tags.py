import dataclasses
import typing as t

from django import http, template
from django.core import paginator
from wagtail.core.models import Page, Site

register = template.Library()


@dataclasses.dataclass
class MenuEntry:
    title: str
    url: str
    is_active: bool

    @classmethod
    def for_page(
        cls,
        page: Page,
        request: http.HttpRequest,
        active_path: str,
    ) -> "MenuEntry":
        url = page.get_url(request=request)
        return cls(title=str(page), url=url, is_active=(active_path.startswith(url)))


@register.inclusion_tag('tags/site_menu.html', takes_context=True)
def site_menu(context, active_path: t.Optional[str] = None):
    request = context['request']
    if active_path is None:
        active_path = request.path

    site = Site.find_for_request(request)
    home_page = site.root_page.specific

    menu_items = [
        MenuEntry(title='Homepage', url=home_page.get_url(request=request), is_active=active_path=='/')
    ] + [
        MenuEntry.for_page(page, request, active_path=active_path)
        for page in home_page.get_children().live().in_menu().specific()
    ]

    return {'menu_items': menu_items}


@dataclasses.dataclass
class PageTree:
    page: Page
    parent: t.Optional["PageTree"]
    children: t.Sequence[Page]


def _as_tree(root: Page, pages: t.Sequence[Page]) -> PageTree:
    root = PageTree(page=root, parent=None, children=[])
    current_parent = root

    for page in pages:
        while not page.is_descendant_of(current_parent.page):
            current_parent = current_parent.parent
        current_node = PageTree(page=page, parent=current_parent, children=[])
        current_parent.children.append(current_node)
        current_parent = current_node

    return root


@register.inclusion_tag('tags/table_of_contents.html', takes_context=True)
def table_of_contents(context, active_page: Page):
    request = context['request']
    site = Site.find_for_request(request)
    home_page = site.root_page

    tree_base = home_page.get_children().ancestor_of(active_page, inclusive=True).specific().get()
    descendants = tree_base.get_descendants().in_menu().live().specific()
    page_tree = _as_tree(tree_base, descendants)

    return {'node': page_tree, 'active_page': active_page}


@register.inclusion_tag('tags/pagination.html', takes_context=True)
def paginate(context: t.Mapping, paginator: paginator.Paginator, page: paginator.Page, base_url: t.Optional[str] = None):
    request = context['request']
    query = request.GET
    if base_url is None:
        base_url = request.path

    return {
        'request': context['request'],
        'paginator': paginator,
        'page': page,
        'links': {
            'first': paginate_link(base_url, query, 1) if page.has_previous() else None,
            'last': paginate_link(base_url, query, paginator.num_pages) if page.has_next() else None,
            'next': paginate_link(base_url, query, page.next_page_number()) if page.has_next() else None,
            'previous': paginate_link(base_url, query, page.previous_page_number()) if page.has_previous() else None,
        },
    }


@register.simple_tag()
def paginate_link(base_url: str, query: http.QueryDict, page_number: int):
    """
    The canonical link for a paginated page. Makes sure the first page doesn't
    have a `page=0` component
    """
    if page_number == 1:
        page_number = None
    return base_url + query_args(query, page=page_number)


@register.filter(name='qs')
def query_args(query: http.QueryDict, **kwargs: t.Dict[str, t.Optional[str]]):
    query = query.copy()

    for key, value in kwargs.items():
        if value is not None:
            query[key] = value
        else:
            query.pop(key, None)

    if len(query) == 0:
        return ''

    return '?' + query.urlencode()
