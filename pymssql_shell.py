#!/usr/bin/env python

"""
A simple shell that allows one to connect to a SQL Server instance via pymssql
and issue queries.

"""

import argparse
import readline   # make raw_input use readline
import sys

import pymssql
from texttable import Texttable


def get_input(prompt):
    if sys.version_info < (3, ):
        return raw_input(prompt)
    else:
        return input(prompt)


def get_query():
    lines = []

    if sys.stdin.isatty():
        prompt = 'SQL> '
    else:
        prompt = ''

    while True:
        input_line = get_input(prompt).strip()
        if len(input_line) == 0 and len(lines) == 0:
            return None
        lines.append(input_line)
        if input_line.endswith(';'):
            break
        prompt = '...> '

    return '\n'.join(lines)


def process_query(conn, query):
    table = Texttable(max_width=0)
    table.set_deco(Texttable.BORDER | Texttable.HEADER | Texttable.VLINES)

    cursor = conn.cursor(as_dict=True)

    try:
        cursor.execute(query)
    except (pymssql.ProgrammingError, pymssql.OperationalError) as e:
        print(str(e))
    else:
        for idx, row in enumerate(cursor.fetchall()):
            if idx == 0:
                table.header(row.keys())

            table.add_row(row.values())

        print(table.draw())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True)
    parser.add_argument('--user', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument('--database', required=True)
    args = parser.parse_args()

    conn = pymssql.connect(host=args.host, user=args.user, password=args.password, database=args.database)

    while True:
        try:
            query = get_query()
        except EOFError:
            # User hit Ctrl+d; quit
            sys.stdout.write("\n")
            break

        if query:
            process_query(conn, query)


if __name__ == '__main__':
    main()

