#!/usr/bin/env python

"""
web handler for sqlitex
"""

# imports
import argparse
import os
import sys
from webob import Request, Response, exc
from wsgiref import simple_server

class Handler(object):
    """WSGI HTTP Handler"""

    def __init__(self, db_file):
        assert os.path.isfile(db_file)

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = Response(content_type='text/plain',
                            body="sqlitex")
        return response(environ, start_response)

def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-p', '--port', dest='port',
                        type=int, default=8080,
                        help="port to serve on")
    options = parser.parse_arguments(args)

    # instantiate WSGI handler
    app = Handler()

    # serve it (Warning! Single threaded!)
    server = simple_server.make_server(host='0.0.0.0',
                                       port=options.port
                                       app=app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()

