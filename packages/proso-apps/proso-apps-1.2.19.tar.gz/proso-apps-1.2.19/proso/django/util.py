from functools import wraps
import hashlib
import logging
import re
from django.core.cache import cache
from django.db import connection

LOGGER = logging.getLogger('django.request')
CACHE_MISS = 'proso-apps-cache-miss'


def disable_for_loaddata(signal_handler):
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs.get('raw'):
            return
        signal_handler(*args, **kwargs)

    return wrapper


def cache_pure(f, expiration=60 * 60 * 24 * 30):
    """ Cache decorator for functions taking one or more arguments. """

    @wraps(f)
    def wrapper(*args, **kwargs):
        if len(args) > 0 and re.match(r"<.+ object at \w+>", repr(args[0])) is not None:
            key_args = [args[0].__class__] + list(args[1:])
        else:
            key_args = args

        key = "{}:args:{}-kwargs:{}".format(f.__name__, repr(key_args), repr(kwargs))
        hash_key = hashlib.sha1(key).hexdigest()
        value = cache.get(hash_key, CACHE_MISS)
        if value != CACHE_MISS:
            LOGGER.debug("loaded function result (%s...) form CACHE; key: %s..., hash %s", str(value)[:300], key[:300], hash_key)
            return value

        value = f(*args, **kwargs)
        LOGGER.debug("saved function result (%s...) to CACHE; key: %s..., hash %s", str(value)[:300], key[:300], hash_key)
        cache.set(hash_key, value, expiration)

        return value

    return wrapper


def is_on_postgresql():
    return connection.settings_dict['ENGINE'] == 'django.db.backends.postgresql_psycopg2'
