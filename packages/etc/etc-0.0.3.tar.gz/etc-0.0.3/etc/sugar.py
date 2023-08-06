# -*- coding: utf-8 -*-
"""
   etc.sugar
   ~~~~~~~~~

   The collection of the sugar functions to increase usability.

"""
from __future__ import absolute_import

from datetime import datetime, timedelta
import threading

import iso8601

from .helpers import Missing


__all__ = ['renew']


def renew(etcd, result, ttl=Missing):
    """Renews the TTL of the node."""
    if ttl is Missing:
        ttl = result.ttl
    return etcd.set(result.key, result.value, ttl=ttl,
                    prev_index=result.modified_index)


def _keep_forever(quit, etcd, result):
    ttl = result.ttl
    delay = max(min(ttl * 2 / 3., ttl - 1), 0)
    while True:
        modified_at = result.expiration - timedelta(seconds=ttl)
        now = datetime.now().replace(tzinfo=iso8601.UTC)
        renew_after = modified_at + timedelta(seconds=delay) - now
        if quit.wait(timeout=renew_after.total_seconds()):
            break
        result = renew(etcd, result, ttl=ttl)
    etcd.delete(result.key, prev_index=result.modified_index)


def keep(etcd, result):
    quit = threading.Event()
    thread = threading.Thread(target=_keep_forever, args=(quit, etcd, result))
    thread.start()
    try:
        thread.join()
    finally:
        quit.set()
