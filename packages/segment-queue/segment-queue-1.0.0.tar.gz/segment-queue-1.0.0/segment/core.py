import datetime
import pickle
import uuid

from analytics.client import ID_TYPES, require
from dateutil.tz import tzutc
from six import string_types

from .consts import EVENT_QUEUE_NAME


class Analytics(object):
    """
    A wrapper class for the Segment library (analytics)

    This class provides drop in replacement methods for some of the Segment API
    and offloads the delivery to a background job. The job is constructed to
    retry delivery until it succeeds, making message delivery reliable.
    """
    def __init__(self, write_key, redis_conn):
        self.redis_conn = redis_conn
        self.write_key = write_key

    def alias(self, previous_id=None, user_id=None, context=None, timestamp=None,
              integrations=None):
        require('previous_id', previous_id, ID_TYPES)
        require('user_id', user_id, ID_TYPES)

        data = {
            'write_key': self.write_key,
            'kwargs': {
                'context': context,
                'integrations': integrations,
                'previousId': previous_id,
                'timestamp': timestamp,
                'type': 'alias',
                'userId': user_id,
            },
        }

        return self._enqueue(data)

    def _enqueue(self, data):
        """
        Enqueue event calls

        Perform some common validation on the tracking data
        """
        if data['kwargs']['context'] is None:
            data['kwargs']['context'] = {}

        if data['kwargs']['integrations'] is None:
            data['kwargs']['integrations'] = {}

        require('context', data['kwargs']['context'], dict)
        require('integrations', data['kwargs']['integrations'], dict)
        require('type', data['kwargs']['type'], string_types)
        user_or_anon = data['kwargs']['userId'] or data['kwargs']['anonymousId']
        require('user_id or anonymous_id', user_or_anon, ID_TYPES)

        # Record the timestamp for when the event occured, not the eventual time at
        # which it gets delivered in the background.
        data['kwargs']['timestamp'] = datetime.datetime.utcnow().replace(tzinfo=tzutc()).isoformat()

        data['kwargs']['messageId'] = str(uuid.uuid4())

        # walk like a duck, quack like a duck
        data['kwargs']['context']['library'] = {
            'name': 'analytics-python',
            'version': '1.0.3'
        }

        pickled_data = pickle.dumps(data)
        self.redis_conn.rpush(EVENT_QUEUE_NAME, pickled_data)

    def identify(self, user_id=None, traits=None, context=None, timestamp=None,
                 anonymous_id=None, integrations=None):
        if user_id is None:
            raise TypeError(u'User ID expected for identify() calls, got None.')

        require('traits', traits, dict)

        data = {
            'write_key': self.write_key,
            'kwargs': {
                'anonymousId': anonymous_id,
                'context': context,
                'integrations': integrations,
                'timestamp': timestamp,
                'traits': traits,
                'type': 'identify',
                'userId': user_id,
            },
        }
        self._enqueue(data)

    def track(self, user_id=None, event=None, properties=None, context=None,
              timestamp=None, anonymous_id=None, integrations=None, ga_client_id=None):
        require('properties', properties, dict)
        require('event', event, string_types)

        data = {
            'write_key': self.write_key,
            'kwargs': {
                'anonymousId': anonymous_id,
                'context': context,
                'event': event,
                'integrations': integrations,
                'properties': properties,
                'type': 'track',
                'userId': str(user_id),
            }
        }

        # Attach the clientId for our server-side events, so we can correlate them
        # to front-end events in Google Analytics
        if ga_client_id is not None:
            data['kwargs']['context'] = {
                'Google Analytics': {
                    'clientId': ga_client_id,
                },
            }

        self._enqueue(data)
