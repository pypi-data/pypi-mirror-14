import datetime
import dateutil.parser
import functools
import logging
import pytz

# it's impossible that "now" is less than this datetime
# we know we are out of sync with real time if we ever
# get a time value less than this
MIN_DT = datetime.datetime(2014, 7, 25, 17, 00, 00)  # Zymbit est date, UTC

utc = pytz.utc

EPOCH = datetime.datetime.utcfromtimestamp(0).replace(tzinfo=utc)

LONG_TIME_AGO = utc.localize(datetime.datetime(1, 1, 1))  # a really long time ago

# keys follow the same convention as InfluxDB
SECOND_PRECISIONS = {
    's': 1,
    'ms': 1000,
    'u': 1e6,
    'n': 1e9,
}


def now():
    return utc.localize(datetime.datetime.utcnow())


def timestamp(dt=None):
    if dt is None:
        dt = now()

    return dt.isoformat('T')


def get_sleep_time(seconds, start):
    """
    Wait at most the given number of seconds from the initial time given
    :param seconds: float - number of seconds to wait
    :param start: datetime - the start time
    :return: float - time to wait
    """
    _now = now()
    delta = _now - start
    diff = delta.seconds + (1.0 * delta.microseconds / 1e6)
    wait = max(0, seconds - diff)

    # print 'start={}, _now={}, delta={}, diff={}, wait={}'.format(start, _now, delta, diff, wait)

    return wait


def interval(interval_delay, default_return=None):
    """
    Call a function every given interval
    :param interval_delay: float - number of seconds
    :param default_return: when the interval has not passed, what to return (default: None)
    """
    interval_delta = datetime.timedelta(seconds=interval_delay)

    def wrapper(fn):
        @functools.wraps(fn)
        def interval_handler(*args, **kwargs):
            t0 = now()
            last_call = getattr(fn, 'last_call', LONG_TIME_AGO)

            if (t0 - last_call) > interval_delta:
                fn.last_call = t0

                return fn(*args, **kwargs)
            else:
                return default_return

        return interval_handler

    return wrapper


class MillisDatetime(object):
    def __init__(self, millis):
        self.last_millis = None
        self.initial = None

        self.set_initial(millis)

    @property
    def logger(self):
        return logging.getLogger(__name__)

    def get_time(self, millis):
        if millis < self.last_millis:
            self.logger.info(
                'time rolled over, last_millis={}, millis={}'.format(
                    self.last_millis, millis))

            self.set_initial(millis)

        delta = datetime.timedelta(milliseconds=millis)
        return self.initial + delta

    def set_initial(self, millis):
        delta = datetime.timedelta(milliseconds=millis)
        self.initial = now() - delta

        self.last_millis = millis


def get_seconds(iso_timestamp, precision='s'):
    """
    Returns the number of seconds since EPOCH for the given ISO 8601 timestamp
    """
    dt = dateutil.parser.parse(iso_timestamp)

    return (dt - EPOCH).total_seconds() * SECOND_PRECISIONS[precision]
