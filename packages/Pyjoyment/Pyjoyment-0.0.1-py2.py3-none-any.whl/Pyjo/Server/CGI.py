# -*- coding: utf-8 -*-

"""
Pyjo.Server.CGI - CGI server
============================
::

    import Pyjo.Server.CGI
    from Pyjo.Util import b

    cgi = Pyjo.Server.CGI.new()
    cgi.unsubscribe('request')

    @cgi.on
    def request(cgi, tx):
        # Request
        method = tx.req.method
        path = tx.req.url.path

        # Response
        tx.res.code = 200
        tx.res.headers.content_type = 'text/plain'
        tx.res.body = b("{0} request for {1}!".format(method, path))

        # Resume transaction
        tx.resume()

    cgi.run()

:mod:`Pyjo.Server.CGI` is a simple and portable implementation of
:rfc:`3875`.

Events
------

:mod:`Pyjo.Server.CGI` inherits all events from :mod:`Pyjo.Server.Base`.

Classes
-------
"""

import Pyjo.Server.Base

import os
import sys
import time

from Pyjo.Util import convert


class Pyjo_Server_CGI(Pyjo.Server.Base.object):
    """
    :mod:`Pyjo.Server.CGI` inherits all attributes and methods from
    :mod:`Pyjo.Server.Base` and implements the following new ones.
    """

    nph = False
    """::

        boolean = cgi.nph
        cgi.nph = boolean

    Activate non-parsed header mode.
    """

    def run(self):
        """::

            status = cgi.run()

        Run CGI.
        """
        tx = self.build_tx()
        req = tx.req.parse(os.environ)
        tx.local_port = os.environ.get('SERVER_PORT', None)
        tx.remote_address = os.environ.get('REMOTE_ADDR', None)

        # Request body (may block if we try to read too much)
        stdin = sys.stdin.buffer if hasattr(sys.stdin, 'buffer') else sys.stdin
        length = convert(req.headers.content_length, int, 0)
        while not req.is_finished:
            buf_size = length if length and length < 131072 else 131072
            buf = bytearray(buf_size)
            read = stdin.readinto(buf)
            if not read:
                break
            req.parse(buf[:read])
            length -= read
            if length <= 0:
                break

        self.emit('request', tx)

        # Response start-line
        res = tx.res.fix_headers()
        if self.nph and not self._write(res, 'get_start_line_chunk'):
            return

        # Response headers
        code = res.code or 404
        msg = res.message or res.default_message()
        if not self.nph:
            res.headers.status = "{0} {1}".format(code, msg)
        if not self._write(res, 'get_header_chunk'):
            return

        # Response body
        if not tx.is_empty and not self._write(res, 'get_body_chunk'):
            return

        # Finish transaction
        tx.server_close()

        return res.code

    def _write(self, res, method):
        offset = 0
        stdout = sys.stdout.buffer if hasattr(sys.stdout, 'buffer') else sys.stdout

        while True:
            # No chunk yet, try again
            chunk = getattr(res, method)(offset)

            if chunk is None:
                time.sleep(1)

            # End of part
            length = len(chunk)
            if not length:
                break

            # Make sure we can still write
            offset += length
            if stdout.closed:
                return False

            stdout.write(chunk)

        return True


new = Pyjo_Server_CGI.new
object = Pyjo_Server_CGI
