python_wsgi_application
------------

Lightweight web application written on Python and based on the wsgiref package, that implements a feedback form with some more views, such as statistics and create / read / delete interfaces for additional parameters.

Project Structure
------------

    templates/           contains HTML templates, used in views
    engine.py            contains web server core
    queries.py           contains SQL queries
    routes.py            contains routes to the public views
    settings.py          contains database settings
    start.py             contains an executable script based on wsgiref
    views.py             contains basic logic for adding and reading data
    wsgi.py              contains function for calling a WSGI application

Requirements
------------

The minimum requirements for this projects is SQLite3 and Python 3.5.

Run
------------

You can run this application through start.py script:

~~~
python3 start.py
~~~
