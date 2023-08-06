from six import iteritems

from yolapy.services import Yola


class Site(object):
    """Represents a Site resource on the Yola API."""

    def __init__(self, **kwargs):
        self._fields = kwargs
        for key, val in iteritems(kwargs):
            setattr(self, key, val)

    def __eq__(self, other):
        return self._fields == other._fields

    @classmethod
    def get(cls, site_id):
        """Get a site from the Yola API."""
        site_attributes = Yola().get_site(site_id)
        return cls(**site_attributes)

    @classmethod
    def list(cls, **filters):
        """Get a list of sites from the Yola API."""
        sites = Yola().list_sites(**filters)['results']
        return [Site(**s) for s in sites]
