#!/usr/bin/python

import os
import time
import sqlite3
from subprocess import PIPE, Popen
from solarshed.controllers.renogy_rover import RenogyRover

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file name
    :return: Connection object or None
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file)        
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():

    database = r"C:\temp\persistence.db"
    sql_create_solar_table = ( 
        "CREATE TABLE IF NOT EXISTS solar ( "
        "dateTime datetime PRIMARY KEY "
        ")"
    )

    conn = create_connection(database)
    create_table(conn, sql_create_solar_table)

if __name__ == '__main__':
    main()

                                  
