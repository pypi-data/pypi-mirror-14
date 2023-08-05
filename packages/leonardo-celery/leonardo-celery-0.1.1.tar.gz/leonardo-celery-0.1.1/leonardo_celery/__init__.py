
from __future__ import absolute_import

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

default_app_config = 'leonardo_celery.Config'

LEONARDO_OPTGROUP = 'Leonardo Celery'
LEONARDO_APPS = [
    'leonardo_celery',
    'djcelery'
]


class Config(AppConfig):
    name = 'leonardo_celery'
    verbose_name = _(LEONARDO_OPTGROUP)

    def ready(self):
        import djcelery
        from celery import Celery

        app = Celery(self.name)

        from django.conf import settings
        app.config_from_object('django.conf:settings')
        app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
        djcelery.setup_loader()
