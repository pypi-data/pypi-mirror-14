"""
my4geks version 0.1.3
https://github.com/denis-ryzhkov/my4geks

Copyright (C) 2015-2016 by Denis Ryzhkov <denisr@denisr.com>
MIT License, see http://opensource.org/licenses/MIT
"""

### import

from adict import adict
from gevent.local import local
from gevent.queue import Queue
from gevent.timeout import Timeout
import pymysql
import sys
import time

### override

pymysql.cursors.DictCursorMixin.dict_type = adict

### db_config

db_config = adict(
    host='127.0.0.1',
    port=3306,
    user='user',
    password='password',
    database='test',
    charset='utf8',
    query_timeout=55, # Less than default web timeout of 60 seconds, but greater than default "innodb_lock_wait_timeout" of 50 seconds.
    pool_size=10,
    _pool=None,
)

### db_init

def db_init():
    db_config._pool = Queue()
    for _ in xrange(db_config.pool_size):
        db_config._pool.put(_create_db_conn())

### _create_db_conn

def _create_db_conn():
    cfg = dict(
        host=db_config.host,
        port=db_config.port,
        user=db_config.user,
        password=db_config.password,
        database=db_config.database,
        cursorclass=pymysql.cursors.DictCursor, # Inherited from "DictCursorMixin" with "dict_type=adict" override done above.
    )
    db_conn = pymysql.connect(**cfg)
    db_conn.set_charset(db_config.charset)
    return db_conn

### _local

_local = local()

### _reconnect

def _reconnect(initial_seconds, max_seconds):
    seconds_before_reconnect = initial_seconds
    while True:

        try:
            _local.db_conn.close()
        except Exception:
            pass

        try:
            _local.db_conn = _create_db_conn()
            break
        except Exception:
            seconds_before_reconnect = min(max_seconds, seconds_before_reconnect * 2)
            time.sleep(seconds_before_reconnect)

    return _local.db_conn

### db_transaction

def db_transaction(code, initial_seconds=0.1, max_seconds=10.0):
    """
    Commits on success.
    Kills slow query, reconnects and raises on timeout.
    Rolls back on any error.
    Reconnects on any error except lock.
    Retries with back off on lock or broken connection.
    Raises other errors.

    Usage:

        def code():
            db(...)
            db(...)
            return result

        result = db_transaction(code)

    NOTE: Context manager like "with db_transaction()" can not loop block inside "with",
    so it doesn't fit for "retry" feature.

    @param function code - Function wrapping DB queries to be executed.
    @param float initial_seconds - Initial time in seconds to sleep before retry/reconnect. Will be doubled each time.
    @param float max_seconds - Upper limit to sleep before reconnect and to stop retrying.
    @return mixed - Whatever "code()" returns.
    """

    ### Check pool.

    if not db_config._pool:
        db_init()

    ### If aready inside a transaction.

    if hasattr(_local, 'db_conn'):
        return code()

    ### Create transaction.

    db_conn = _local.db_conn = db_config._pool.get(block=True)
    try: # Always return to the pool in "finally".

        ### Retry while needed. Will be stopped below.

        seconds_before_retry = initial_seconds
        while True:
            try:
                ### Commits on success.

                db_conn.begin()
                result = code()
                db_conn.commit()
                return result

            ### Kills slow query, reconnects and raises on timeout.

            except Timeout:
                e_type, e_value, e_traceback = sys.exc_info()
                slow_id = db_conn.thread_id()
                db_conn = _reconnect(initial_seconds, max_seconds)

                try:
                    db_conn.kill(slow_id)
                except Exception:
                    pass

                raise e_type, e_value, e_traceback

            ### error

            except Exception:
                e_type, e_value, e_traceback = sys.exc_info()
                e_repr = repr(e_value)

                is_lock = (
                    'Deadlock found when trying to get lock' in e_repr or
                    'Lock wait timeout exceeded; try restarting transaction' in e_repr
                )
                is_broken = (
                    'Connection reset by peer when receiving' in e_repr or
                    'Lost connection to MySQL server' in e_repr or
                    'MySQL server has gone away' in e_repr or
                    "Can't find record in" in e_repr or
                    'Command Out of Sync' in e_repr or
                    'InterfaceError' in e_repr or
                    'Not connected' in e_repr or
                    'Broken pipe' in e_repr
                ) # TODO: Add explicit cases on demand. Probably some cases of OperationalError should not be retried.

                ### Rolls back on any error.

                try:
                    db_conn.rollback()
                except Exception:
                    pass

                ### Reconnects on any error except lock.

                if not is_lock:
                    db_conn = _reconnect(initial_seconds, max_seconds)

                ### Retries with back off on lock or broken connection.

                if (is_lock or is_broken) and seconds_before_retry < max_seconds:
                    time.sleep(seconds_before_retry)
                    seconds_before_retry = min(max_seconds, seconds_before_retry * 2)
                    continue # Retry.

                ### Raises other errors.

                raise e_type, e_value, e_traceback

    ### Return connection to the pool.

    finally:
        # "Reconnect" above tries until success, so this connection is NOT broken.
        db_config._pool.put(db_conn)
        del _local.db_conn

### db

def db(sql, *values, **params):
    """
    Queries DB and returns result.

    @param str sql - SQL with %s placehodlers.
        Do NOT add quotes or IN-brackets around %s.
        E.g. db('...WHERE `name` IN %s', [value1, value2])

    @param tuple values - Values for %s placehodlers.

    @param dict params:
        str charset - E.g. "utf8mb4" for tables with Emoji.

    @return adict:
        list(adict) rows - All rows in result.
        adict|NoneType row - First row, if any.
        int affected - Number of rows affected.
    """

    charset = params.get('charset', db_config.charset)

    def code():

        if _local.db_conn.charset != charset:
            _local.db_conn.set_charset(charset)

        with _local.db_conn.cursor() as cursor:
            with Timeout(db_config.query_timeout):
                cursor.execute(sql, values)
            return cursor.fetchall(), cursor.rowcount

    rows, affected = db_transaction(code)
        # It's just "rows, affected = code()" if already inside a transaction.

    return adict(
        rows=rows,
        row=rows[0] if rows else None,
        affected=affected,
    )
