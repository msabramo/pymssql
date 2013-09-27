import datetime
import gevent
import os
import pymssql
#import random

server = os.getenv("PYMSSQL_TEST_SERVER")
user = os.getenv("PYMSSQL_TEST_USERNAME")
password = os.getenv("PYMSSQL_TEST_PASSWORD")
database = os.getenv("PYMSSQL_TEST_DATABASE")

def run(num):
#    gevent.sleep(random.randint(0, 2) * 0.001)

    # if num in (1, 2, 3, 4):
    #     gevent.sleep()

    # Insert artificial sleeps to simulate yielding from other I/O
    # to create a case where greenish performs terribly
    # for i in range(num  * 2):
    #     print("%s yielding (%d) ..." % (num, i))
    #     gevent.sleep()

    now = datetime.datetime.now()
    print("%s connecting at time: %s" % (num, now))
    conn = pymssql.connect(host=server,
                           database=database,
                           user=user,
                           password=password)
    cur = conn.cursor()
    cur.execute("""WAITFOR DELAY '00:00:0%d'; SELECT CURRENT_TIMESTAMP -- greenlet %d""" % (5, num))
    row = cur.fetchone()
    print("    CURRENT_TIMESTAMP = %r" % (row[0],))
    # if num in (0, 2, 4):
    #     print("    *** num == %d; going to do another query..." % num)
    #     cur.execute("""WAITFOR DELAY '00:00:0%d'; SELECT CURRENT_TIMESTAMP """ % 5)
    #     row = cur.fetchone()
    #     print("    CURRENT_TIMESTAMP = %r" % (row[0],))
    conn.close()

def do_test():
    greenlets = []

    dt1 = datetime.datetime.now()

    for i in range(5):
        greenlets.append(gevent.spawn(run, i))

    gevent.joinall(greenlets)

    dt2 = datetime.datetime.now()

    print("Done running - elapsed time: %s" % (dt2 - dt1))


if False:
    print("**** Running test WITHOUT gevent.sleep wait_callback...\n")
    do_test()

print("\n***** Running test WITH gevent.sleep wait_callback...\n")

def wait_callback(conn, query_str):
    print("    *** wait_callback called with conn = %r, query_str = %r" % (conn, query_str))
    gevent.sleep()

pymssql.set_wait_callback(wait_callback)

do_test()
