from django.test import TestCase

from wagtail.wagtailcore.models import Page

from ..utils import suggest_page_from_misspelled_slug


class SuggestPageFromMisspelledSlugTest(TestCase):

    def test_no_similar_slugs_returns_none(self):
        result = suggest_page_from_misspelled_slug(
            '/no-such-page/', None)
        assert result is None

    def test_matching_slug_returns_page(self):
        home_page = Page.objects.get(slug='home')
        article = Page(
            title='Workzone with Bridget Masinga',
            slug='workzone-with-bridget-masinga'
        )
        home_page.add_child(instance=article)

        result = suggest_page_from_misspelled_slug(
            '/workzon-bridget-masing/', home_page)

        assert result == article

    def test_multiple_matches_returns_best_matching_page(self):
        home_page = Page.objects.get(slug='home')
        better_matching_article = Page(
            title='Workzone with Bridget Masinga',
            slug='workzone-with-bridget-masinga'
        )
        poorer_matching_article = Page(
            title='Bridget Masinga',
            slug='bridget-masinga'
        )
        home_page.add_child(instance=better_matching_article)
        home_page.add_child(instance=poorer_matching_article)

        result = suggest_page_from_misspelled_slug(
            '/workzon-bridget-masing/', home_page)

        assert result == better_matching_article
