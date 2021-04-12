from wagtail.core.models import Page

from jaxattax.utils import breadcrumbs_for_page


class PageWithBreadcrumbs(Page):
    class Meta:
        abstract = True

    def get_context(self, request, *args, **kwargs):
        return {
            **super().get_context(request, *args, **kwargs),
            "breadcrumbs": breadcrumbs_for_page(self, request),
        }
