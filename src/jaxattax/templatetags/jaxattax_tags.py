import dataclasses
import typing as t

from django import forms, http, template
from django.core import paginator
from wagtail.core.models import Page, Site

from jaxattax.donations.models import CashDonation

register = template.Library()


@dataclasses.dataclass
class PageTree:
    page: Page
    parent: t.Optional["PageTree"]
    children: t.Sequence[Page]


@dataclasses.dataclass
class MenuEntry:
    title: str
    url: str
    is_active: bool
    menu_id: t.Optional[str] = None
    children: t.Sequence["MenuEntry"] = dataclasses.field(default_factory=list)

    @classmethod
    def for_page(
        cls,
        page: Page,
        request: http.HttpRequest,
        active_path: str,
        children: t.Iterable["MenuEntry"] = (),
    ) -> "MenuEntry":
        url = page.get_url(request=request)
        return cls(
            title=str(page),
            url=url,
            is_active=active_path.startswith(url),
            menu_id=f'menu-id-{page.pk}',
            children=list(children),
        )

    @classmethod
    def for_page_tree(
        cls,
        page_tree: PageTree,
        request: http.HttpRequest,
        active_path: str,
    ) -> "MenuEntry":
        return MenuEntry.for_page(
            page=page_tree.page,
            request=request,
            active_path=active_path,
            children=(
                MenuEntry.for_page_tree(child, request, active_path)
                for child in page_tree.children
            )
        )


def _as_tree(root: Page, pages: t.Sequence[Page]) -> t.List[PageTree]:
    root = PageTree(page=root, parent=None, children=[])
    current_parent = root

    for page in pages:
        while not page.is_descendant_of(current_parent.page):
            current_parent = current_parent.parent
        current_node = PageTree(page=page, parent=current_parent, children=[])
        current_parent.children.append(current_node)
        current_parent = current_node

    return root.children


@register.inclusion_tag('tags/site_menu.html', takes_context=True)
def site_menu(context, active_path: t.Optional[str] = None):
    request = context['request']
    if active_path is None:
        active_path = request.path

    site = Site.find_for_request(request)
    home_page = site.root_page.specific
    descendants = home_page.get_descendants().in_menu().live().specific()

    children = _as_tree(home_page, descendants)

    menu_items = [
        MenuEntry(title='Homepage', url=home_page.get_url(request=request), is_active=active_path=='/')
    ] + [
        MenuEntry.for_page_tree(page_tree, request=request, active_path=active_path)
        for page_tree in children
    ]

    return {'menu_items': menu_items}


@register.inclusion_tag('tags/table_of_contents.html', takes_context=True)
def table_of_contents(context, active_page: Page):
    request = context['request']
    site = Site.find_for_request(request)
    home_page = site.root_page

    descendants = active_page.get_descendants().in_menu().live().specific()
    children = _as_tree(active_page, descendants)

    return {'children': children, 'active_page': active_page}


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


@register.filter
def add_class(bound_field: forms.BoundField, classes: str) -> forms.BoundField:
    attrs = bound_field.field.widget.attrs
    if 'class' in attrs:
        attrs['class'] = f'{attrs["class"]} {classes}'
    else:
        attrs['class'] = classes
    return bound_field


@register.inclusion_tag('tags/form_field.html', takes_context=True)
def form_field(
    context: t.Mapping,
    bound_field: forms.BoundField,
    *,
    group_class: t.Optional[str] = None,
    prefix: t.Optional[str] = None,
    suffix: t.Optional[str] = None,
) -> dict:
    field_context = {
        'is_hidden': bound_field.is_hidden,
        'bound_field': bound_field,
        'label': str(bound_field.label),
        'field_id': bound_field.id_for_label,
        'group_class': ' ' + group_class if group_class else ''
    }

    if isinstance(bound_field.field.widget, forms.CheckboxInput):
        field_context.update({
            'is_checkbox': True,
            'field': str(add_class(bound_field, 'form-check-input')),
        })

    else:
        field_context.update({
            'field': str(add_class(bound_field, 'form-control')),
        })

    if bound_field.help_text:
        description_id = bound_field.id_for_label + '-description'
        bound_field.field.widget.attrs['aria-describedby'] = description_id
        field_context.update({
            'description': bound_field.help_text,
            'description_id': description_id,
        })

    if prefix or suffix:
        field_context.update({
            'surround': True,
            'prefix': prefix,
            'suffix': suffix,
        })

    return field_context


@register.simple_tag
def get_cash_donations():
    return [
        {'name': c.name, 'amount': c.amount, 'date': c.date}
        for c in CashDonation.objects.all().order_by('-date', '-created')
    ]
