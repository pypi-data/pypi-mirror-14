
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
