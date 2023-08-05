import redis
import simplejson
import settings


def push_event(event_data, channels=()):
    """
    Helper method to push events to websocket server from python applications by using Redis
    Uses separate thread to make requests.
    :param event_data: Event data (JSON parsable object)
    :param channels: List of Redis channels to which the event will be pushed
    :return: numbers of subscribers that received an event
    """

    assert settings.REDIS_SERVER, "settings.REDIS_SERVER is not defined"
    assert settings.REDIS_SERVER_PORT, "settings.REDIS_SERVER_PORT is not defined"

    r = redis.StrictRedis(host=settings.REDIS_SERVER, port=settings.REDIS_SERVER_PORT, db=0)
    recipents = 0
    for channel in channels:
        recipents += r.publish(channel, simplejson.dumps(event_data))

    return recipents
