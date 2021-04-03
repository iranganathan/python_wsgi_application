# -*- coding: utf-8 -*-
import os
import sys
import sqlite3
import traceback
from wsgiref.simple_server import WSGIRequestHandler
import signal

import settings
import logging

views_folder = 'templates'
view_base = os.path.join(views_folder, 'base.html')
base_path = os.path.dirname(os.path.realpath(__file__))

FORMAT = u'%(levelname)s: %(filename)s [line: %(lineno)d] [%(asctime)s]: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


class Shutdowner:
    def __init__(self):
        self.shutdown = False
        signal.signal(signal.SIGINT, self.exit)
        signal.signal(signal.SIGTERM, self.exit)

    def exit(self, signum, frame):
        self.shutdown = True


class CustomWSGIRequestHandler(WSGIRequestHandler):
    def log_message(self, format, *args):
        logging.info("%s - %s\n" % (self.client_address[0], format % args))


class Cursor:
    def __init__(self):
        def row_factory(cur, row):
            row_dictionary = {}
            for idx, col in enumerate(cur.description):
                row_dictionary[col[0].lower()] = row[idx]
            return row_dictionary

        # connect to the database
        if settings.DATABASE['ENGINE'] == "sqlite":
            conn = sqlite3.connect(os.path.join(base_path, settings.DATABASE['NAME'] + ".db"))
            # set row_factory function to convert rows to dictionaries
            conn.row_factory = row_factory
            cursor = conn.cursor()
        else:
            raise Exception("Database %s is not supported!" % settings.DATABASE['ENGINE'])

        self.connection = conn
        self.cursor = cursor

    def execute(self, sql, values=None, single=False, commit=False):
        logging.debug("SQL query:" + sql)
        if values:
            logging.debug("Values: " + str(values))
        records = []
        values = values if values else {}
        for rec in self.cursor.execute(sql, values):
            records.append(rec)

        if single and len(records):
            records = records[0]

        if commit:
            self.commit()

        return records

    def commit(self):
        logging.debug('COMMIT')
        self.connection.commit()


class Context:
    def __init__(self, environ=None, get=None, post=None):
        self.environ = environ
        self.GET = get
        self.POST = post

        cur = Cursor()

        self.cursor = cur


def create_db(context):
    if settings.DATABASE['ENGINE'] == "sqlite":
        cur = context.cursor
        db_exists = cur.execute("""
            SELECT 1
            FROM SQLITE_MASTER
            WHERE TYPE = 'table'
        """, single=True)
        if not db_exists:
            sql_file = open(os.path.join(base_path, settings.DATABASE['NAME'] + '.sql'), 'r', encoding='utf-8')
            sql_file_text = sql_file.read()
            sql_file.close()

            sql_commands = sql_file_text.split(';')

            # execute each SQL-command from file
            for command in sql_commands:
                cur.execute(command)
            cur.commit()


def print_error():
    exc_type, exc_value, exc_traceback = sys.exc_info()

    print('An error occurred during script execution!')
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)


def render(view_name='', parameters=None):
    with open(os.path.join(base_path, view_base), 'r', encoding='utf-8') as base_view_file:
        base_view = base_view_file.read()

    if view_name != '':
        with open(os.path.join(base_path, views_folder, view_name), 'r', encoding='utf-8') as view_file:
            view = view_file.read()

        html_body = view % parameters
    else:
        html_body = ''

    html_page = base_view % {
        'title': parameters['title'],
        'body': html_body
    }

    return html_page
