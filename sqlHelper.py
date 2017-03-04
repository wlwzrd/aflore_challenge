import sqlite3
from sqlite3 import Error

__author__ = "Mario Gutierrez/wlwzrd"
__email__ = "mfdogutierrez@gmail.com"

DB_name = 'ebay_categories.db'
SQL_createTable = """ CREATE TABLE IF NOT EXISTS category_T (
                                        category_ID INTEGER PRIMARY KEY,
                                        category_Name TEXT NOT NULL,
                                        category_Level INTEGER,
                                        best_OfferEnabled TEXT,
                                        category_ParentID INTEGER,
                                        FOREIGN KEY(category_ParentID) REFERENCES category_T(category_ID)
                                    ); """

def insertSQL(cID,cName,cLevel,bOE,cParentID):
    """ create an insert sql
    :param cID: Category ID
    :param cName: Category Name
    :param cLevel: Category Level
    :param bOE: Best Offer Enabled
    :param cParentID: Category Parent ID
    :return: created sql statement
    """
    sql = 'INSERT INTO category_T VALUES (' + cID + ',"' + cName + '",' + cLevel + ',"' + bOE + '",' + cParentID + ')'
    return sql

def createConnection(db):
    """ create a database connection to the SQLite3 database
    :param db: database file/name
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db)
        return conn
    except Error as e:
        print("Error while connecting to the  database")
        print e
    return None 

def runSQL(conn, sql):
    """ create a table based on the  sql statement
    :param conn: Connection object
    :param sql: a SQL query
    """
    log = []
    try:
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        return True
    except Error as e:
        log.append(["Error while running SQL in database",e,sql])
        print log
    return False
