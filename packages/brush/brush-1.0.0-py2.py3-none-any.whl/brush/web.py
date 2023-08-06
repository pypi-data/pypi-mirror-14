"""Web interface for brush."""

import os.path
import logging
from concurrent.futures import ThreadPoolExecutor
import json
from datetime import datetime

from tornado import gen
from tornado.options import options
from tornado.web import Application, RequestHandler, MissingArgumentError
from tornado.concurrent import run_on_executor
from tornado.escape import url_unescape

from . import uimodules, models
from .models import select_timeseries
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
    executor = ThreadPoolExecutor(max_workers=4)

    def initialize(self, engine, table):
        self.engine = engine
        self.table = table

    def _jsonize(self, col, data):
        if isinstance(data[0], datetime):
            data = [(dt - datetime(1970, 1, 1)).total_seconds() for dt in data]
            return data
        else:
            return data

    @run_on_executor
    def get_data(self, start, stop=None):
        """Retrieve data from the database server."""
        with self.engine.connect() as conn:
            sel = select_timeseries(self.table, start, stop)
            rows = conn.execute(sel).fetchall()
        if len(rows) == 0:
            return dict(error='No data; try an earlier start time')
        columns = self.table.columns.keys()
        row_data = list(zip(*rows))
        data = {col: self._jsonize(col, row_data[i]) for i, col in enumerate(columns)}
        return data

    @gen.coroutine
    def get(self):
        """Get data starting from the timestamp ``start`` up until the
        timestamp ``stop``. Timestamps must be given in `ISO 8601`__
        format and passed as query arguments in the ``GET`` request.

        If only ``start`` is given, the stop point is the current time.

        Example::

           http://localhost:8090/data?start=20160411T0900

        .. note:: The database stores timestamps in UTC. It is up to
                  the client to correctly account for this.

        __ https://en.wikipedia.org/wiki/ISO_8601

        """
        try:
            start = url_unescape(self.get_query_argument('start'))
        except MissingArgumentError:
            self.send_error(400)
            return

        try:
            stop = url_unescape(self.get_query_argument('stop'))
        except MissingArgumentError:
            stop = None

        # TODO: implement specifying columns to return
        # try:
        #     keys = self.get_query_argument('keys')
        #     keys = keys.split(',')
        # except MissingArgumentError:
        #     keys = None

        try:
            data = yield gen.maybe_future(self.get_data(start, stop))
            self.set_header('content-type', 'application/json')
            self.write(json.dumps(data, sort_keys=True))
        except Exception as e:
            self.send_error(400)
            logger.error(str(e))


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


def make_app(engine, prefix=None, static_path=default_static_path):
    """Initialize the Tornado web app.

    Parameters
    ----------
    engine
        SQLAlchemy engine
    prefix : str or None
        URL prefix for routing
    static_path : str
        Path to static files (JS, CSS, images, etc.)

    """
    handlers = [
        ['/', MainHandler],
        ['/data', DataHandler, dict(engine=engine, table=models.brush)],
        ['/data/current', CurrentDataHandler],
        ['/data/recent', RecentDataHandler],
        ['/data/query/(.*)', QueryHandler],
        ['/query/(.*)', QueryHandler]  # kept for backwards compatibility
    ]
    if prefix not in [u'', None]:
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
