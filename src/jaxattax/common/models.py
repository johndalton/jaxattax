import wagtail.core.models

from jaxattax.utils.breadcrumbs import breadcrumbs_for_page


class Page(wagtail.core.models.Page):
    """Base class for all Wagtail Pages in this site"""
    class Meta:
        abstract = True

    def get_breadcrumbs(self, request):
        return breadcrumbs_for_page(self, request)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if 'breadcrumbs' not in context:
            context['breadcrumbs'] = self.get_breadcrumbs(request)
        return context
