"""Web interface for brush."""

import os.path
import logging
import time

from tornado import gen
from tornado.options import options
from tornado.web import Application, RequestHandler, MissingArgumentError

from . import uimodules
from .db import InfluxClient
from .stores import store

logger = logging.getLogger('web')

base_dir = os.path.dirname(__file__)
default_static_path = os.path.abspath(
    os.path.join(base_dir, 'static'))
template_path = os.path.abspath(
    os.path.join(base_dir, 'templates'))


class MainHandler(RequestHandler):
    def get(self):
        """Main page for displaying real-time data."""
        self.render('status.html')


class DataHandler(RequestHandler):
    def initialize(self, database):
        assert isinstance(database, InfluxClient)
        self.database = database

    @gen.coroutine
    def get_data(self, start, stop=None):
        """Retrieve data from the database server."""
        try:
            if stop is None:
                data = yield self.database.get_data_since(start)
            else:
                if stop < start or start > time.time():
                    data = 400
                data = yield self.database.get_data_between(start, stop)
        except Exception as e:
            raise e
        raise gen.Return(data)

    @gen.coroutine
    def get(self):
        """Get data starting from the timestamp ``start`` up until the
        timestamp ``stop``. These timestamps should be passed as query
        arguments in the ``GET`` request, though only ``start`` is
        required. If ``stop`` is not given, all data starting from
        ``start`` is returned. If a ``keys`` query argument is
        provided, only return data matching those keys (comma
        separated).

        """
        try:
            start = float(self.get_query_argument('start'))
        except MissingArgumentError:
            self.send_error(400)
            return

        try:
            stop = float(self.get_query_argument('stop'))
        except MissingArgumentError:
            stop = None

        try:
            keys = self.get_query_argument('keys')
            keys = keys.split(',')
        except MissingArgumentError:
            keys = None

        try:
            data = yield self.get_data(start, stop)
            if data == 400:
                self.send_error(400)
        except Exception as e:
            self.send_error(400)
            raise e
        else:
            self.write(data)


class QueryHandler(RequestHandler):
    def get(self, key):
        """Return the most recent value for the requested key."""
        try:
            value = store.get()[key]
            self.write({
                key: value,
                'error': None
            })
        except KeyError:
            self.write({'error': 'No such key'})


class CurrentDataHandler(RequestHandler):
    def get(self):
        """Return the most recent data."""
        data = store.get()
        data['error'] = None
        self.write(data)


class RecentDataHandler(RequestHandler):
    def get(self):
        """Return all data currently in the store."""
        try:
            data = store.get(amount=-1)
            data['error'] = None
        except:
            data = dict(error="Server error. Check logs.")
        self.write(data)


def make_app(database, prefix=None, static_path=default_static_path):
    """Initialize the Tornado web app.

    :param InfluxClient database:
    :param list keys: available data keys
    :param str prefix: URL prefix for routing
    :param bool debug: enable debug mode if True

    """
    handlers = [
        ['/', MainHandler],
        ['/data', DataHandler, dict(database=database)],
        ['/data/current', CurrentDataHandler],
        ['/data/recent', RecentDataHandler],
        ['/data/query/(.*)', QueryHandler],
        ['/query/(.*)', QueryHandler]  # kept for backwards compatibility
    ]
    if prefix is not '' and prefix is not None:
        if prefix[0] != '/':
            prefix = '/' + prefix
        for handler in handlers:
            route = handler[0]
            if route == '/':
                handler[0] = prefix
            else:
                handler[0] = prefix + route

    app = Application(
        handlers,
        template_path=template_path,
        static_path=static_path,
        ui_modules=uimodules,
        debug=options.debug
    )
    return app
