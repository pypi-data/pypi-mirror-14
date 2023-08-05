from django.shortcuts import render

from .utils import suggest_page_from_misspelled_slug


def not_found(request):  # pragma: no cover
    slug = request.path
    root_page = request.site.root_page.specific

    suggested_page = suggest_page_from_misspelled_slug(slug, root_page)

    data = {'suggested_page': suggested_page}
    return render(request, '404.html', data, status=404)
