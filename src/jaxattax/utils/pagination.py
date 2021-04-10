from django.core.paginator import EmptyPage, Paginator


def paginate(request, items):
    paginator = Paginator(items, 5)

    try:
        page_number = int(request.GET['page'])
        page = paginator.page(page_number)
    except (ValueError, KeyError, EmptyPage):
        page = paginator.page(1)

    return paginator, page
