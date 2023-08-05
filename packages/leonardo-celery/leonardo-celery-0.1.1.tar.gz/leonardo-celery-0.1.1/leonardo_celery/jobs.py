
try:
    from cacheback.base import Job
except ImportError:
    raise Exception(
        "You haven't cacheback please"
        " run pip install leonardo-celery['cacheback']")


class FetchContent(Job):

    """Mix it with ``ContentProxyWidget`` for async cache update
    """

    @property
    def expiry(self):
        return self.cache_validity

    def fetch(self, *args, **kwargs):
        """call ``get_data`` which is similar to this method
        """
        return self.get_data(*args, **kwargs)

    @property
    def data(self):
        """return actual content
        """
        return self.get()
