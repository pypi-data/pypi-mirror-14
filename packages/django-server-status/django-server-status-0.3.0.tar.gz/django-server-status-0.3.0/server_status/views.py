"""
Status checks

Notes:

* Useful messages are logged, but NO_CONFIG is returned whether
  settings are missing or invalid, to prevent information leakage.
* Different services provide different information, but all should return
  UP, DOWN, or NO_CONFIG for the "status" key.
"""
from __future__ import unicode_literals
from datetime import datetime
import logging

import celery
from django.conf import settings
from django.http import JsonResponse, Http404

log = logging.getLogger(__name__)

UP = "up"
DOWN = "down"
NO_CONFIG = "no config found"
HTTP_OK = 200
SERVICE_UNAVAILABLE = 503
TIMEOUT_SECONDS = 5


# pylint: disable=too-many-locals
def get_pg_info():
    """Check PostgreSQL connection."""
    from psycopg2 import connect, OperationalError
    log.debug("entered get_pg_info")
    try:
        conf = settings.DATABASES['default']
        database = conf["NAME"]
        user = conf["USER"]
        host = conf["HOST"]
        port = conf["PORT"]
        password = conf["PASSWORD"]
    except (AttributeError, KeyError):
        log.error("No PostgreSQL connection info found in settings.")
        return {"status": NO_CONFIG}
    except TypeError:
        return {"status": DOWN}
    log.debug("got past getting conf")
    try:
        start = datetime.now()
        connection = connect(
            database=database, user=user, host=host,
            port=port, password=password, connect_timeout=TIMEOUT_SECONDS,
        )
        log.debug("at end of context manager")
        micro = (datetime.now() - start).microseconds
        connection.close()
    except (OperationalError, KeyError) as ex:
        log.error("No redis connection info found in settings. %s Error: %s",
                  conf, ex)
        return {"status": DOWN}
    log.debug("got to end of postgres check successfully")
    return {"status": UP, "response_microseconds": micro}


def get_redis_info():
    """Check Redis connection."""
    from kombu.utils.url import _parse_url as parse_redis_url
    from redis import (
        StrictRedis,
        ConnectionError as RedisConnectionError,
        ResponseError as RedisResponseError,
    )
    try:
        url = settings.BROKER_URL
        _, host, port, _, password, database, _ = parse_redis_url(url)
    except AttributeError as ex:
        log.error("No redis connection info found in settings. Error: %s", ex)
        return {"status": NO_CONFIG}

    start = datetime.now()
    try:
        rdb = StrictRedis(
            host=host, port=port, db=database,
            password=password, socket_timeout=TIMEOUT_SECONDS,
        )
        info = rdb.info()
    except (RedisConnectionError, TypeError) as ex:
        log.error("Error making Redis connection: %s", ex.args)
        return {"status": DOWN}
    except RedisResponseError as ex:
        log.error("Bad Redis response: %s", ex.args)
        return {"status": DOWN, "message": "auth error"}
    micro = (datetime.now() - start).microseconds
    del rdb  # the redis package does not support Redis's QUIT.
    ret = {
        "status": UP, "response_microseconds": micro,
    }
    fields = ("uptime_in_seconds", "used_memory", "used_memory_peak")
    ret.update({x: info[x] for x in fields})
    return ret


def get_elasticsearch_info():
    """Check Elasticsearch connection."""
    from elasticsearch import (
        Elasticsearch,
        ConnectionError as ESConnectionError
    )
    try:
        url = settings.HAYSTACK_CONNECTIONS["default"]["URL"]
    except (AttributeError, KeyError) as ex:
        log.error("No elasticsearch connection info found in settings. "
                  "Error: %s", ex)
        return {"status": NO_CONFIG}
    start = datetime.now()
    try:
        search = Elasticsearch(url, request_timeout=TIMEOUT_SECONDS)
        search.info()
    except ESConnectionError:
        return {"status": DOWN}
    del search  # The elasticsearch library has no "close" or "disconnect."
    micro = (datetime.now() - start).microseconds
    return {
        "status": UP, "response_microseconds": micro,
    }


def get_celery_info():
    """
    Check celery availability
    """
    if not getattr(settings, 'USE_CELERY', False):
        log.error("No celery config found. Set USE_CELERY in settings to enable.")
        return {"status": NO_CONFIG}
    start = datetime.now()
    try:
        # pylint: disable=no-member
        celery_stats = celery.task.control.inspect().stats()
        if not celery_stats:
            log.error("No running Celery workers were found.")
            return {"status": DOWN, "message": "No running Celery workers"}
    except IOError as exp:
        log.error("Error connecting to the backend: %s", exp)
        return {"status": DOWN, "message": "Error connecting to the backend"}
    return {"status": UP, "response_microseconds": (datetime.now() - start).microseconds}


def status(request):  # pylint: disable=unused-argument
    """Status"""
    token = request.GET.get("token", "")
    if token != settings.STATUS_TOKEN:
        raise Http404()

    info = {}
    check_mapping = {
        'REDIS': (get_redis_info, 'redis'),
        'ELASTIC_SEARCH': (get_elasticsearch_info, 'elasticsearch'),
        'POSTGRES': (get_pg_info, 'postgresql'),
        'CELERY': (get_celery_info, 'celery'),
    }

    for setting, (check_fn, key) in check_mapping.items():
        if setting in settings.HEALTH_CHECK:
            log.debug('getting: %s', key)
            info[key] = check_fn()
            log.debug('%s done', key)

    code = HTTP_OK
    status_all = UP
    for key in info:
        if info[key]["status"] == DOWN:
            code = SERVICE_UNAVAILABLE
            status_all = DOWN
            break

    info["status_all"] = status_all

    resp = JsonResponse(info)
    resp.status_code = code
    return resp
