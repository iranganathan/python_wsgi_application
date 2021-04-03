# -*- coding: utf-8 -*-
from urllib import parse
import views
from routes import routes
from engine import print_error, Context
from wsgiref.util import setup_testing_defaults


# function for calling a WSGI application
def application(environ, start_response):
    setup_testing_defaults(environ)

    # parsing GET-query
    get_query = parse.parse_qs(environ['QUERY_STRING'])

    # parsing POST-query
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size)
    request_body_decoded = parse.unquote(request_body.decode('utf-8'))
    post_query = parse.parse_qs(request_body_decoded, encoding='utf-8')

    context = Context(environ, get_query, post_query)

    response_headers = [('Content-type', 'text/html')]

    # get the controller name from an URL
    controller_name = environ['PATH_INFO']
    if controller_name in routes:
        try:
            if controller_name == '/':
                controller_name = '/index'
            controller = getattr(views, controller_name[1:])
            response_body = controller(context)
            status = '200 OK'
        except:
            print_error()
            response_body = views.error_500(context)
            status = '500 Internal Server Error'
    else:
        response_body = views.error_404(context)
        status = '404 Not Found'

    # initialize the server response
    start_response(status, response_headers)

    # return the response body
    return [response_body.encode('utf-8')]
