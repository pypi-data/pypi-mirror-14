from wagtail.wagtailcore.models import Page


def suggest_page_from_misspelled_slug(slug, root_page):
    sql = '''SELECT p.*, similarity(slug, %(slug)s) AS similarity
             FROM wagtailcore_page p
             WHERE slug %% %(slug)s
             ORDER BY similarity DESC
             LIMIT 1'''
    page = Page.objects.raw(sql, {'slug': slug})
    suggested_page = None

    # page is currently a RawQuerySet...
    if list(page) and root_page in page[0].get_ancestors().specific():
        suggested_page = page[0].specific

    return suggested_page
