""" database access
docs:
* http://initd.org/psycopg/docs/
* http://initd.org/psycopg/docs/pool.html
* http://initd.org/psycopg/docs/extras.html#dictionary-like-cursor
"""
## adapted and modified from the example given to us in class from Session07 - Adding a Database

from contextlib import contextmanager
import logging
import os

from flask import current_app, g

import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor

pool = None

def setup():
    global pool
    DATABASE_URL = os.environ['DATABASE_URL']
    ##current_app.logger.info(f"creating db connection pool")
    pool = ThreadedConnectionPool(1, 5, dsn=DATABASE_URL, sslmode='require')

@contextmanager
def get_db_connection():
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)


@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
      cursor = connection.cursor(cursor_factory=DictCursor)
      # cursor = connection.cursor()
      try:
          yield cursor
          if commit:
              connection.commit()
      finally:
          cursor.close()


## QUERIES FOR HW1
def add_person (favChar, favItem, favLevel, checked, explanation, date):
    with get_db_cursor(True) as cur:
        cur.execute("INSERT INTO responses (id, favCharacter, favItem, favLevel, checked, explanationForKart, dateOfEntry) values (DEFAULT,%s, %s, %s, %s, %s, %s)", (favChar, favItem, favLevel, checked, explanation, date))


def fetch_response_data():
    with get_db_cursor() as cur:
        cur.execute('select * from responses')
        return cur.fetchall()

def fetch_response_data_backwards():
    with get_db_cursor() as cur:
        cur.execute('SELECT * FROM responses r ORDER BY r.dateOfEntry DESC')
        return cur.fetchall()