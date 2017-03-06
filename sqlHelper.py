import sqlite3
from sqlite3 import Error

__author__ = "Mario Gutierrez/wlwzrd"
__email__ = "mfdogutierrez@gmail.com"

DB_name = 'ebay_categories.db'

SQL_createNestedTable = """ CREATE TABLE IF NOT EXISTS categoryN (
                                        category_ID INTEGER PRIMARY KEY,
                                        category_Name TEXT NOT NULL,
                                        category_Level INTEGER,
                                        best_OfferEnabled TEXT,
                                        category_ParentID INTEGER,
                                        lft INTEGER NOT NULL,
                                        rgt INTEGER NOT NULL,
                                        FOREIGN KEY(category_ParentID) REFERENCES category_T(category_ID));"""

SQL_falseParent = """INSERT INTO categoryN VALUES (0,'FalseParent',0,'False',0,1,2)"""

def createConnection(db):
    """ create a database connection to the SQLite3 database
    :param db: database file/name
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db)
        return conn
    except Error as e:
        print "ERROR: Ccconnecting to the  database: ", e
    return None 

def runSQL(conn, sql):
    """ create a table based on the  sql statement
    :param conn: Connection object
    :param sql: a SQL query
    """
    try:
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
    except Error as e:
        print "ERROR runSQL: ", e

def countSQL(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM categoryN")
        r = cur.fetchall()
        count = r[0][0]
        return count
    except Error as e:
        print e

def insertNode(conn,cID,cName,cLevel,bOE,cParentID):
    try:
        print "INSERTING: ", cID,cName, cLevel, bOE, cParentID
        cursor = conn.cursor()
        if int(cLevel) == 1:
            getFalseParent = ("SELECT lft, rgt FROM categoryN WHERE lft = 1")
            cursor.execute(getFalseParent)
            rows = cursor.fetchall()
        elif int(cLevel) > 1:
            getParentNode = "SELECT lft, rgt FROM categoryN WHERE category_ID = " + str(cParentID) + ";"
            cursor.execute(getParentNode)
            rows = cursor.fetchall()
        lftP = rows[0][0]
        rgtP = rows[0][1]
        sqlUpdateRgt = "UPDATE categoryN SET rgt = rgt+2 WHERE rgt >= " + str(rgtP) +  ";"
        sqlUpdateLft = "UPDATE categoryN SET lft = lft+2 WHERE lft >= " + str(rgtP) +  ";"
        sqlInsertNew = 'INSERT INTO categoryN VALUES ('+ cID +',"'+ cName +'",'+ cLevel +',"'+ bOE +'",'+ cParentID +','+ str(rgtP) +','+ str(rgtP+1) +')'
        cursor.execute(sqlUpdateRgt)
        cursor.execute(sqlUpdateLft)
        cursor.execute(sqlInsertNew)
        conn.commit()
    except Error as e:
        print "NODE PARENT:", e,  cID

def getCategories(conn, categoryID):
    """ 
    """
    try:
        cur = conn.cursor()
        getParentNode = "SELECT lft, rgt FROM categoryN WHERE category_ID = " + str(categoryID) + ";"
        cur.execute(getParentNode)
        rows = cur.fetchall()
        lftP = rows[0][0]
        rgtP = rows[0][1]
        sqlGetAll = "SELECT category_ID, category_Name, category_Level, category_ParentID  FROM categoryN WHERE lft BETWEEN " + str(lftP) + " AND " + str(rgtP)
        cur.execute(sqlGetAll)
        rows = cur.fetchall()
        return rows
    except Error as e:
        print e
