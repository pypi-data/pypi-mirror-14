"""Command-line interface for brush."""

import logging

from tornado.options import options
from tornado.ioloop import IOLoop

from .comb import FrequencyComb, DummyFrequencyComb
from .sweep import Sweep

logger = logging.getLogger('brush')


def main():
    """Command-line interface entry point."""
    options.parse_command_line()

    if options.offline:
        comb = DummyFrequencyComb()
        options.debug = True
    else:
        comb = FrequencyComb(options.xmlrpc_host, options.xmlrpc_port,
                             options.xmlrpc_user, options.xmlrpc_password)

    sweep = Sweep(comb)
    IOLoop.instance().run_sync(lambda: sweep.run())

if __name__ == "__main__":
    main()
