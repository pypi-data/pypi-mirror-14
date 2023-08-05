#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from woost.tests.models.basetestcase import BaseTestCase


class WebsiteHostMatchingTestCase(BaseTestCase):

    def test_can_match_more_than_one_host(self):

        from woost.models import Website

        w1 = Website()
        w1.hosts.append("foo.com")
        w1.hosts.append("foo.net")
        self.config.websites.append(w1)

        w2 = Website()
        w2.hosts.append("bar.com")
        w2.hosts.append("spam.bar.com")
        self.config.websites.append(w2)

        assert self.config.get_website_by_host("foo.com") is w1
        assert self.config.get_website_by_host("foo.net") is w1
        assert self.config.get_website_by_host("bar.com") is w2
        assert self.config.get_website_by_host("spam.bar.com") is w2

    def test_solves_collissions_by_relative_order_of_websites_in_configuration(self):

        from woost.models import Website

        w1 = Website()
        w1.hosts.append("bar.com")
        w1.hosts.append("foo.com")
        self.config.websites.append(w1)

        w2 = Website()
        w2.hosts.append("foo.com")
        self.config.websites.append(w2)

        assert self.config.get_website_by_host("foo.com") is w1


class WebsiteLanguageTestCase(BaseTestCase):

    def test_websites_can_override_language_visibility(self):

        from woost.models import Configuration, Website, set_current_website

        w1 = Website()
        w2 = Website()

        self.config.languages = ["ca", "es", "en"]

        for website in (None, w1, w2):
            set_current_website(website)
            for lang in ["ca", "es", "en"]:
                assert self.config.language_is_enabled(lang)

        self.config.published_languages = ["en"]

        for website in (None, w1, w2):
            set_current_website(website)
            assert self.config.language_is_enabled("en")
            assert not self.config.language_is_enabled("ca")
            assert not self.config.language_is_enabled("es")

        w1.published_languages = ["ca"]

        set_current_website(w1)
        assert self.config.language_is_enabled("ca")
        assert not self.config.language_is_enabled("es")
        assert not self.config.language_is_enabled("en")

        set_current_website(w2)
        assert self.config.language_is_enabled("en")
        assert not self.config.language_is_enabled("ca")
        assert not self.config.language_is_enabled("es")


class WebsiteSpecificContentTestCase(BaseTestCase):

    def test_descendants_inherit_availability(self):

        from woost.models import Website, Document

        w1 = Website()
        w2 = Website()

        d1 = Document()
        d1.websites = [w1]

        d2 = Document()
        d2.websites = [w2]
        d2.parent = d1
        assert list(d2.websites) == [w1]

        d3 = Document()
        d3.parent = d2
        assert list(d3.websites) == [w1]

        d1.websites.append(w2)
        assert list(d2.websites) == [w1, w2]
        assert list(d3.websites) == [w1, w2]

        d1.websites = []
        assert not d2.websites
        assert not d3.websites

    def test_designating_a_website_home_implies_exclusivity(self):

        from woost.models import Website, Document

        d1 = Document()
        w1 = Website()
        w1.home = d1
        assert list(d1.websites) == [w1]

    def test_websites_own_document_trees_exclusively(self):

        from woost.models import Website, Document

        d1 = Document()

        w1 = Website()
        w1.home = d1

        w2 = Website()
        w2.home = d1

        assert list(d1.websites) == [w2]


class WebsiteSpecificContentIndexingTestCase(BaseTestCase):

    def test_content_is_not_indexed_until_inserted(self):

        from woost.models import Website, Publishable

        index = Publishable.per_website_publication_index

        w1 = Website()
        w1.insert()

        p1 = Publishable()
        assert not list(index.items())

        p1.websites = [w1]
        assert not list(index.items())

    def test_content_is_not_indexed_until_website_is_inserted(self):

        from woost.models import Website, Publishable

        index = Publishable.per_website_publication_index

        w1 = Website()

        p1 = Publishable()
        p1.insert()
        p1.websites = [w1]

        assert (w1.id, p1.id) not in list(index.items())

    def test_content_is_published_for_all_websites_by_default(self):

        from woost.models import Website, Publishable

        index = Publishable.per_website_publication_index

        w1 = Website()
        w1.insert()

        p1 = Publishable()
        p1.insert()

        assert list(index.items()) == [(None, p1.id)]

        p2 = Publishable()
        p2.insert()

        assert set(index.items()) == set([(None, p1.id), (None, p2.id)])

    def test_content_can_change_its_designated_websites(self):

        from woost.models import Website, Publishable

        index = Publishable.per_website_publication_index

        p1 = Publishable()
        p1.insert()

        w1 = Website()
        w1.insert()

        w2 = Website()
        w2.insert()

        assert list(index.items()) == [(None, p1.id)]

        p1.websites = [w1]
        assert list(index.items()) == [(w1.id, p1.id)]

        p1.websites = [w2]
        assert list(index.items()) == [(w2.id, p1.id)]

        p1.websites = [w1, w2]
        assert set(index.items()) == set([(w1.id, p1.id), (w2.id, p1.id)])

        p1.websites = []
        assert list(index.items()) == [(None, p1.id)]

    def test_index_is_updated_after_deleting_publishable(self):

        from woost.models import Website, Publishable

        index = Publishable.per_website_publication_index

        p1 = Publishable()
        p1.insert()
        p1.delete()

        assert (None, p1.id) not in list(index.items())

        w1 = Website()
        w1.insert()

        p2 = Publishable()
        p2.websites = [w1]
        p2.insert()
        p2.delete()

        assert not list(index.items())

    def test_index_is_updated_after_deleting_website(self):

        from woost.models import Website, Publishable

        index = Publishable.per_website_publication_index

        w1 = Website()
        w1.insert()

        w2 = Website()
        w2.insert()

        p1 = Publishable()
        p1.websites = [w1]
        p1.insert()

        p2 = Publishable()
        p2.websites = [w1, w2]
        p2.insert()

        w1.delete()
        assert set(index.items()) == set([(None, p1.id), (w2.id, p2.id)])

        w2.delete()
        assert set(index.items()) == set([(None, p1.id), (None, p2.id)])

