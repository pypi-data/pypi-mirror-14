import json
import pickle
import pprint

import requests
from analytics.request import DatetimeSerializer
from click import echo, style

from .consts import EVENT_QUEUE_NAME, UNDELIVERED_EVENT_QUEUE_NAME


RETRY_BATCH_SIZE = 20


def deliver_events(redis_conn, burst=False, verbose=False):
    """
    Tries to deliver events one by one to segment.  If it fails,
    reschedules the event for repeated delivery until it succeeds.
    """
    if burst:
        echo('Delivering all outstanding events.')
    else:
        echo('Waiting for events...')

    while True:
        if burst:
            pickled_data = redis_conn.lpop(EVENT_QUEUE_NAME)
            if not pickled_data:
                break
        else:
            result = redis_conn.blpop(EVENT_QUEUE_NAME, timeout=60)
            if not result:
                continue
            _, pickled_data = result

        # Don't catch any exceptions here.  If anything here fails, this means we
        # prepared the queue with corrupt or incompatible information, so we want
        # to know about this through regular exception reporting.
        unpickled_data = pickle.loads(pickled_data)
        kwargs = unpickled_data['kwargs']

        if verbose:
            echo(pprint.pformat(kwargs))

        auth = (unpickled_data['write_key'], '')
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'batch': [kwargs]}, cls=DatetimeSerializer)
        url = 'https://api.segment.io/v1/batch'
        r = requests.post(url, data=data, auth=auth, headers=headers)

        if r.ok:
            echo('Successfully delivered "{}" (userId={})'.format(kwargs['messageId'], kwargs['userId']))
            echo('')
            continue

        echo('{}: {}'.format(style('Error', fg='red'), r.content))
        redis_conn.lpush(UNDELIVERED_EVENT_QUEUE_NAME, pickled_data)
        echo('{}: Moved to undeliverable queue.'.format(style('Warning', fg='yellow')))

    echo('Done.')


def retry_undelivered_events(redis_conn):
    """
    Moves all undelivered events back into our event output queue.  Should be
    called periodically.

    Protect against thundering herd issues by limiting the number of retries
    per job invocation.  This also protects against flooding so other job
    types would get pushed back.
    """
    with redis_conn.pipeline() as p:
        for _ in range(RETRY_BATCH_SIZE):
            p.rpoplpush(UNDELIVERED_EVENT_QUEUE_NAME, EVENT_QUEUE_NAME)
        results = p.execute()

    num_moved = len([r for r in results if r])
    if num_moved:
        echo('Rescheduled {} events to retry delivery.'.format(num_moved))
