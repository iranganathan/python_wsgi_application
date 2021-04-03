from wsgiref.simple_server import make_server
from wsgi import application
from engine import Context, create_db
from engine import CustomWSGIRequestHandler, Shutdowner
import logging

is_running = True

if __name__ == '__main__':
    port = 8080
    logging.info("Server started on port " + str(port))
    shutdowner = Shutdowner()

    # create a database if not exists
    context = Context()
    create_db(context)

    httpd = make_server("localhost", port, application, handler_class=CustomWSGIRequestHandler)

    while True:
        httpd.handle_request()
        if shutdowner.shutdown:
            break
