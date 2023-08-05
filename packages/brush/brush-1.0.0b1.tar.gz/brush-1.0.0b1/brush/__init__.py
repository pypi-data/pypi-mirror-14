import os.path as osp
from tornado.options import define, options

__version__ = "1.0.0b1"

define('debug', default=False, help='Enable debug output')
define('offline', default=False, help='Run in offline mode')
define('config', default='~/.brush.conf', help='Path to configuration file',
       callback=lambda path: read_config_file(path))

define('xmlrpc-host', type=str, help='XMLRPC server hostname')
define('xmlrpc-port', type=int, default=8123, help='XMLRPC server port')
define('xmlrpc-user', default=None, help='XMLRPC server user')
define('xmlrpc-password', default=None, help='XMLRPC server password')

define('influx-host', default='localhost', help='InfluxDB ')
define('influx-port', default=8086, help='InfluxDB port')
define('influx-https', default=False, help='Use https for InfluxDB')
define('influx-database', default='comb', help='InfluxDB database')
define('influx-user', default=None, help='InfluxDB user')
define('influx-password', default=None, help='InfluxDB password')

define('redis-host', default='localhost', help='Redis hostname')
define('redis-port', default=6379, help='Redis port')
define('redis-password', default=None, help='Redis password')

define('server-port', default=8090, help='Port to serve on')
define('server-url-prefix', default='', help='URL prefix')


def read_config_file(path):
    """Open a configuration file and return it as a dict."""
    if not osp.exists(osp.abspath(osp.expanduser(path))):
        return
    else:
        options.parse_config_file(path, final=False)
