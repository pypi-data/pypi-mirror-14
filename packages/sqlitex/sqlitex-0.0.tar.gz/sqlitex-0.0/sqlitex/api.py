"""
sqlitex API
"""

# imports
import argparse
import csv
import os
import sqlite3
import sys
from StringIO import StringIO

class SQLitEx(object):

    def __init__(self, db_file):
        self.db_file = os.path.abspath(db_file)
        if not os.path.isfile(self.db_file):
            raise AssertionError("Not a file: '{0}'".format(self.db_file))

    def __call__(self, query):
        con = sqlite3.connect(self.db_file)
        cursor = con.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def tables(self):
        """
        return a list of tables; see
        http://stackoverflow.com/questions/305378/get-list-of-tables-db-schema-dump-etc-in-sqlite-databases
        """
        tables = self("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [i[0] for i in tables]
        return tables

    def contents(self, table):
        rows = self("SELECT * FROM {table};".format(table=table))
        return rows

    def describe(self, table):
        con = sqlite3.connect(self.db_file)
        cursor = con.cursor()
        cursor.execute("SELECT * FROM {table} LIMIT 1;".format(table=table))
        header = [i[0] for i in cursor.description]
        return header

def rows2csv(rows, fp=None):
    """convert rows to csv"""

    return_string = False
    if fp is None:
        return_string = True
        fp = StringIO()
    writer = csv.writer(fp)
    writer.writerows(rows)
    fp.flush()
    if return_string:
        return fp.getvalue()


def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('db_file',
                        help="path to sqlite database file")
    parser.add_argument('table', nargs='?', default=None,
                        help="table to output")

    options = parser.parse_args(args)

    # instantiate api
    api = SQLitEx(options.db_file)

    if options.table:
        rows = api.contents(options.table)
        header = api.describe(options.table)
        rows.insert(0, header)
        print (rows2csv(rows))
    else:
        # list tables
        tables = api.tables()
        print ('\n'.join(tables))

if __name__ == '__main__':
    main()
