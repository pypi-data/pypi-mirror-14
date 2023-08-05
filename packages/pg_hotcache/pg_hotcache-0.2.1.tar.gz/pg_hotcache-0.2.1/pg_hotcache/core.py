from __future__ import print_function
from __future__ import absolute_import
import getpass
import psycopg2
import psycopg2.extras
import sys
from . import __version__
from argparse import ArgumentParser
from re import compile


def load_cache(args):
    if not args.host:
        conn_string = "dbname='{0}' user='{1}' password='{2}'".format(
            args.dbname, args.username, args.password
        )
    else:
        conn_string = "host='{0}' port='{1}' dbname='{2}' user='{3}' password='{4}'".format(
            args.host, args.port, args.dbname, args.username, args.password
        )
    try:
        conn = psycopg2.connect(conn_string)
    except psycopg2.Error as e:
        if "password authentication failed" in str(e):
            password = getpass.getpass("Password for user {0}: ".format(args.username))
            if not args.host:
                conn_string = "dbname='{0}' user='{1}' password='{2}'".format(
                    args.dbname, args.username, password
                )
            else:
                conn_string = "host='{0}' port='{1}' dbname='{2}' user='{3}' password='{4}'".format(
                    args.host, args.port, args.dbname, args.username, password
                )
            try:
                conn = psycopg2.connect(conn_string)
            except psycopg2.Error as e:
                print(e)
                sys.exit(1)
        else:
            print(e)
            sys.exit(1)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute("""show server_version""")
    except psycopg2.Error as e:
        print(e)
        sys.exit(1)
    rows = cur.fetchall()
    version = rows[0][0].split('.')
    support_text = "Minimal supported PostgreSQL version is 9.4. " \
                   "Your PostgreSQL version is {0}.{1}.{2}".format(*version)
    if version[0] == '9':
        if int(version[1]) < 4:
            print(support_text)
            sys.exit(1)
    if int(version[0]) < 9:
        print(support_text)
        sys.exit(1)
    B = {
        'kB': 1,
        'MB': 2,
        'GB': 3,
        'TB': 4
    }
    pg_units = compile(r'([\d])+({0}|{1}|{2}|{3})'.format(*B.keys()))
    try:
        cur.execute(
            """
            SELECT setting, unit
            FROM pg_settings
            WHERE name='effective_cache_size'
            """
        )
    except psycopg2.Error as e:
        print(e)
        sys.exit(1)
    rows = cur.fetchall()
    eff_cache_size_setting = int(rows[0][0])
    eff_cache_size_unit = str(rows[0][1])
    unit_opts = pg_units.findall(eff_cache_size_unit)
    effective_cache_size = eff_cache_size_setting * int(unit_opts[0][0]) * 1024 ** B[unit_opts[0][1]]
    try:
        cur.execute(
            """
            SELECT relname, pg_relation_size(relid)
            FROM pg_stat_all_tables
            WHERE relname not like 'pg_%' and relname not like 'sql_%'
            ORDER BY COALESCE(seq_scan, 0)+COALESCE(idx_scan, 0) DESC;
            """
        )
    except psycopg2.Error as e:
        print(e)
        sys.exit(1)
    rows = cur.fetchall()
    db_tables_count = len(rows)
    if db_tables_count == 0:
        print("No tables in the database {0}".format(args.dbname))
        sys.exit()
    tables = list()
    i = 0
    summary_size = 0
    while summary_size < effective_cache_size and i < len(rows):
        summary_size += rows[i][1]
        tables.append(rows[i][0])
        i += 1
    if summary_size > effective_cache_size:
        tables.pop()
        i -= 1
    if not tables:
        print('Either too small parameter "effective_cache_size" or too large tables')
        sys.exit()
    for table in tables:
        print("load table {0} into cache".format(table))
        try:
            cur.execute(
                """
                select pg_prewarm('{0}')
                """.format(table)
            )
        except psycopg2.Error as e:
            if "No function matches the given name and argument types" in str(e):
                print(
"""
Error: In the database is not installed the extension pg_prewarm.
To add an extension pg_prewarm need to install the package postgresql-contrib.
After you need to connect to the database under the superuser and run the command:
create extension pg_prewarm;"""
                )
            else:
                print(e)
            sys.exit(1)
    print("{0} of the {1} tables are loaded into cache".format(i, db_tables_count))


def main():
    p = ArgumentParser(
        description='Loading into cache from said PostgreSQL database the tables, which are most frequently scanned.\n'
                    'Limiter for loading into cache is the value of "effective_cache_size".',
        epilog='version = {0}'.format(__version__),
        add_help=False,
    )
    p.add_argument('-?', '--help', action="help",
                   help="show this help message and exit")
    p.add_argument('-h', '--host', action='store',
                   help='database server host or socket directory (default: "local socket")')
    p.add_argument('-p', '--port', action='store', default=5432, type=int,
                   help='database server port (default: "5432")')
    p.add_argument('-U', '--username', action='store', default=getpass.getuser(),
                   help='database user name (default: "{0}")'.format(getpass.getuser()))
    p.add_argument('-W', '--password', action='store',
                   help='force password prompt (should happen automatically)')
    p.add_argument('-d', '--dbname', action='store', required=True,
                   help='database name for caching')
    args = p.parse_args()
    load_cache(args)

if __name__ == "__main__":
    main()
