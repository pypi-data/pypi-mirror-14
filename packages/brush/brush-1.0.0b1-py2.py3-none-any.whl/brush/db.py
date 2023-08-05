"""Save and query data with InfluxDB."""

import logging
import json
import time
from tornado import gen
from tornado.escape import url_escape
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

logger = logging.getLogger('db')


class QueryError(Exception):
    """Raised when a database query error occurs."""


class InfluxClient(object):
    def __init__(self, host='localhost', database='comb',
                 user=None, password=None, https=False, port=8086):
        protocol = 'https' if https else 'http'
        self.db = database
        self.user = user
        self.password = password
        self.base_url = '{protocol:s}://{host:s}:{port:d}'.format(
            protocol=protocol, host=host, port=port)
        self.client = AsyncHTTPClient()

    def _make_request(self, url, body=None, method='GET'):
        request = HTTPRequest(url, method=method, body=body,
                              auth_username=self.user,
                              auth_password=self.password)
        return request

    def _make_line(self, key, fields, tags=None, timestamp=None):
        assert isinstance(key, str)
        assert isinstance(fields, dict)
        assert tags is None or isinstance(tags, dict)
        assert timestamp is None or isinstance(timestamp, float)
        line = key
        if tags is not None:
            line = line + ',' + ','.join(['{}={}'.format(tag, tags[tag]) for tag in tags])
        line = line + ' ' + ','.join(['{}={}'.format(field, fields[field]) for field in fields])
        if timestamp is not None:
            line = '%s %.0f' % (line, timestamp * 1e9)
        logger.debug('Line protocol string: ' + line)
        return line

    @gen.coroutine
    def _write(self, line):
        url = self.base_url + '/write?db=' + self.db
        request = self._make_request(url, line, method='POST')
        # response = yield self.client.fetch(request)  # why doesn't this work?
        response = yield AsyncHTTPClient().fetch(request, raise_error=False)
        if response.code >= 500:
            logger.error('Error code %d: Severe problem with InfluxDB server' % response.code)
        elif 400 >= response.code > 500:
            logger.error('Error code %d: Invalid request to InfluxDB' % response.code)
        elif 200 >= response.code > 300:
            if response.code == 200:
                logger.error(response.body)
            elif response.code == 204:
                logger.debug('Successful write to InfluxDB')
        else:
            logger.debug('InfluxDB return code ' + str(response.code))

    @gen.coroutine
    def write(self, measurement, fields, tags=None, timestamp=None):
        """Write a single measurement to the database.

        Parameters
        ----------
        measurement : str
            Measurement to record
        fields : dict
            Measurement values for a single timestamp to write
        tags : dict or None
            Metadata for the measurement
        timestamp : float or None
            Seconds since the epoch in UTC

        """
        line = self._make_line(measurement, fields, tags, timestamp)
        yield self._write(line)

    @gen.coroutine
    def write_points(self, points):
        """Write many points at once.

        Parameters
        ----------
        points : list
            A list of dicts containing the keys ``measurement`` and
            ``fields`` and optionally ``tags`` and ``timestamp``. See
            :meth:`write` for details.

        """
        assert isinstance(points, (list, tuple))
        lines = []
        for point in points:
            measurement = point['measurement']
            fields = point['fields']
            tags = point.get('tags', None)
            timestamp = point.get('timestamp', None)
            lines.append(self._make_line(measurement, fields, tags, timestamp))
        lines = '\n'.join(lines)
        yield self._write(lines)

    @gen.coroutine
    def query(self, query_string):
        """Query the database with an arbitrary query string.

        Parameters
        ----------
        query_string : str
            See https://docs.influxdata.com/influxdb/v0.10/guides/querying_data/

        Returns
        -------
        data : dict
            JSON-deserialized response from the server.

        Raises
        ------
        QueryError
            when the database returns an error

        """
        query_string = url_escape(query_string)
        url = self.base_url + '/query?db={}&q={}'.format(self.db, query_string)
        logger.debug(url)
        request = self._make_request(url)
        response = yield AsyncHTTPClient().fetch(request)
        if response.code != 200 and response.code != 400:
            raise RuntimeError('Error: ' + str(response.code))
        data = json.loads(response.body.decode())
        if 'error' in data:
            logger.error(data['error'])
            raise QueryError(data['error'])
        raise gen.Return(data)

    @gen.coroutine
    def get_data_between(self, start, stop):
        """Get data between timestamps start and stop."""
        query = "SELECT * FROM comb WHERE time > %.0f AND time < %.0f".format(
            start * 1e9, stop * 1e9)
        logger.debug(query)
        data = yield self.query(query)
        raise gen.Return(data)

    @gen.coroutine
    def get_data_since(self, timestamp):
        """Get data from the given timestamp and now."""
        query = "SELECT * FROM comb WHERE time > %.0f AND time < now()".format(
            timestamp * 1e9)
        logger.debug(query)
        data = yield self.query(query)
        raise gen.Return(data)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from tornado.ioloop import IOLoop
    import random
    client = InfluxClient(host='localhost', database='test')

    @gen.coroutine
    def main():
        yield client.write('test', {'value': random.random()}, {'thing': 'stuff'})
        data = yield client.query("SELECT * FROM test WHERE thing='stuff'")
        print(data)

    IOLoop.current().run_sync(main)
