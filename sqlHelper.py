import sqlite3

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

def SQL_insert():
    sql = """ INSERT """

def createConnection(db):
    """ create a database connection to the SQLite3 database
    :param db: database file/name
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db)
        return conn
    except:
        print("Error while creating database")
    return None 

def runSQL(conn, sql):
    """ create a table based on the  sql statement
    :param conn: Connection object
    :param sql: a CREATE TABLE statement
    """
    try:
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
    except:
        print("Error while CRUD in database")
