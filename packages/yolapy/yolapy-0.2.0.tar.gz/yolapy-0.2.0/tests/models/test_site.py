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
