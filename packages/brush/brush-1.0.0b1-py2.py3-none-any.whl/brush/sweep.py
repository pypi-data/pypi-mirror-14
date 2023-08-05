import logging
import signal
import json

from tornado import gen
from tornado.options import options
from tornado.locks import Event

from . import db
from .comb import DummyFrequencyComb, FrequencyComb
from .web import make_app
from .stores import store

logger = logging.getLogger('brush')

try:
    import redis
except ImportError:
    logger.warning('redis not found... will not try to write to Redis.')
    redis = None


class Sweep(object):
    """Get data from the frequency comb XMLRPC server and log it to a
    database.

    """
    def __init__(self, comb):
        assert isinstance(comb, (DummyFrequencyComb, FrequencyComb))
        self.comb = comb

        # Initialize databases
        self.db = db.InfluxClient(host=options.influx_host,
                                  database=options.influx_database,
                                  user=options.influx_user,
                                  password=options.influx_password,
                                  https=options.influx_https,
                                  port=options.influx_port)
        self._init_redis()

        # Start the web server
        self.done = Event()
        self.app = make_app(self.db, prefix=options.server_url_prefix)
        self.app.listen(options.server_port)
        signal.signal(signal.SIGINT, lambda num, frame: self.done.set())
        logger.info('Listening on port ' + str(options.server_port))

    def _init_redis(self):
        """Connect to redis if applicable."""
        self.redis = None
        if redis is not None:
            try:
                self.redis = redis.StrictRedis(host=options.redis_host,
                                               port=options.redis_port,
                                               password=options.redis_password)
            except Exception:
                logger.error(
                    'Error configuring or connecting to Redis. Disabling.')

    @gen.coroutine
    def run(self):
        """Periodically polls the comb server for data."""
        last_timestamp = None
        while not self.done.is_set():
            data = self.comb.get_data()
            timestamp = data['timestamp']

            # Don't rewrite data
            if timestamp == last_timestamp:
                yield gen.sleep(0.01)
                continue
            last_timestamp = timestamp

            data = {key.replace('.', '_').lower(): data[key] for key in data}
            store.append(data)
            data.pop('timestamp')

            tags = dict()
            for key in data:
                if any(k in key for k in ['system_locked', '_status', 'plo_ok']):
                    tags[key] = data[key]
            [data.pop(key) for key in tags]
            if not options.offline:
                yield self.db.write(measurement='comb', fields=data,
                                    tags=tags, timestamp=timestamp)

            if self.redis is not None:
                self.redis.set('brush', json.dumps(data))

            if options.offline:
                yield gen.sleep(1)
