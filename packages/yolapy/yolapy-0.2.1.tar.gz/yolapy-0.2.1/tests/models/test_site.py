from unittest import TestCase

from mock import patch

from yolapy.models import Site


class SiteTestCase(TestCase):
    def setUp(self):
        yola_patcher = patch('yolapy.models.site.Yola')
        self.yola = yola_patcher.start().return_value
        self.addCleanup(yola_patcher.stop)


class TestSite(SiteTestCase):
    def test_sets_init_kwargs_as_attributes(self):
        site = Site(name='my site', id='123')
        self.assertEqual(site.name, 'my site')
        self.assertEqual(site.id, '123')


class TestSiteGet(SiteTestCase):
    """Site.get"""

    def test_instantiates_site_with_attrs_from_service(self):
        self.yola.get_site.return_value = {'name': 'site name', 'id': '456'}

        site = Site.get('456')

        self.yola.get_site.assert_called_once_with('456')
        self.assertEqual(site.name, 'site name')
        self.assertEqual(site.id, '456')


class TestSiteList(SiteTestCase):
    """Site.list"""

    def test_instantiates_list_of_sites_with_attrs_from_service(self):
        self.yola.list_sites.return_value = {'results': [
            {'id': '1'}, {'id': '2'},
        ]}

        sites = Site.list()

        self.assertEqual(len(sites), 2)
        self.assertIn(Site(id='1'), sites)
        self.assertIn(Site(id='2'), sites)

    def test_filters_sites_by_passed_fields(self):
        Site.list(user_id='user123')
        self.yola.list_sites.assert_called_once_with(user_id='user123')
