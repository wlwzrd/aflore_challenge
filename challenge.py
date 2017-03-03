import urllib
import httplib
import sqlite3
import os
import sys
import getopt
#import requests 

from xml.dom.minidom import parse, parseString

__author__ = "Mario Gutierrez/wlwzrd"
__email__ = "mfdogutierrez@gmail.com"


g_FuncName = "GetCategories"
g_AppID = "EchoBay62-5538-466c-b43b-662768d6841"
g_CertID = "00dd08ab-2082-4e3c-9518-5f4298f296db"
g_DevID = "16aGetCategories26b1b-26cf-442d-906d-597b60c41c19"
g_SiteID = "0"
g_DetailLevel = "0"
g_Host = "api.sandbox.ebay.com"
g_HostURL = "/ws/api.dll"
g_unsignedToken = "AgAAAA**AQAAAA**aAAAAA**PMIhVg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4GhCpaCpQWdj6x9nY+seQ**L0MCAA**AAMAAA**IahulXaONmBwi/Pzhx0hMqjHhVAz9/qrFLIkfGH5wFH8Fjwj8+H5FN4NvzHaDPFf0qQtPMFUaOXHpJ8M7c2OFDJ7LBK2+JVlTi5gh0r+g4I0wpNYLtXnq0zgeS8N6KPl8SQiGLr05e9TgLRdxpxkFVS/VTVxejPkXVMs/LCN/Jr1BXrOUmVkT/4Euuo6slGyjaUtoqYMQnmBcRsK4xLiBBDtiow6YHReCJ0u8oxBeVZo3S2jABoDDO9DHLt7cS73vPQyIbdm2nP4w4BvtFsFVuaq6uMJAbFBP4F/v/U5JBZUPMElLrkXLMlkQFAB3aPvqZvpGw7S8SgL7d2s0GxnhVSbh4QAqQrQA0guK7OSqNoV+vl+N0mO24Aw8whOFxQXapTSRcy8wI8IZJynn6vaMpBl5cOuwPgdLMnnE+JvmFtQFrxa+k/9PRoVFm+13iGoue4bMY67Zcbcx65PXDXktoM3V+sSzSGhg5M+R6MXhxlN3xYfwq8vhBQfRlbIq+SU2FhicEmTRHrpaMCk4Gtn8CKNGpEr1GiNlVtbfjQn0LXPp7aYGgh0A/b8ayE1LUMKne02JBQgancNgMGjByCIemi8Dd1oU1NkgICFDbHapDhATTzgKpulY02BToW7kkrt3y6BoESruIGxTjzSVnSAbGk1vfYsQRwjtF6BNbr5Goi52M510DizujC+s+lSpK4P0+RF9AwtrUpVVu2PP8taB6FEpe39h8RWTM+aRDnDny/v7wA/GkkvfGhiioCN0z48"


def getEbayXml():
    """Connects to the Ebay API
    :return: xml response from the API call
    """

    headers = {
        'X-EBAY-API-CALL-NAME': g_FuncName.encode("utf-8"),
        'X-EBAY-API-APP-NAME': g_AppID.encode("utf-8"),
        'X-EBAY-API-CERT-NAME': g_CertID.encode("utf-8"),
        'X-EBAY-API-DEV-NAME': g_DevID.encode("utf-8"),
        'X-EBAY-API-SITEID': g_SiteID.encode("utf-8"),
        'X-EBAY-API-COMPATIBILITY-LEVEL': '861',
        "Content-Type": "text/xml; charset=utf-8"
    }
    xmlIn = "<?xml version='1.0' encoding='utf-8'?>"+\
            "<GetCategoriesRequest xmlns='urn:ebay:apis:eBLBaseComponents'>"+\
            "<RequesterCredentials>"+\
            "<eBayAuthToken>" + g_unsignedToken  + "</eBayAuthToken>"+\
            "</RequesterCredentials>"+\
            "<CategorySiteID>" + g_SiteID.encode("utf-8")  + "</CategorySiteID>"+\
            "<DetailLevel>ReturnAll</DetailLevel>"+\
            "</GetCategoriesRequest>"
    xmlOut = None
    try:
        conn = httplib.HTTPSConnection(g_Host)
        conn.request("POST", g_HostURL, xmlIn.encode('utf-8'), headers)
        response = conn.getresponse()
        xmlOut = response.read()
        conn.close()
    except Exception, ex:
        print ex
    return xmlOut
    
def create_connection(db):
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

def table_CRUD(conn, sql):
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
def generate_insert_sql():
    sql = """INSERT"""

def build():
    db = 'ebay_categories.db'
    sql_createTable = """ CREATE TABLE IF NOT EXISTS category_T (
                                        category_ID INTEGER PRIMARY KEY,
                                        category_Name TEXT NOT NULL,
                                        category_Level INTEGER,
                                        best_OfferEnabled TEXT,
                                        category_ParentID INTEGER,
                                        FOREIGN KEY(category_ParentID) REFERENCES category_T(category_ID) 
                                    ); """
    xmlOut = getEbayXml()
    response = parseString(xmlOut)
    categories = response.getElementsByTagName('Category')
    # categories[numero de categorias].childNodes[0..5].childNodes[0].data
    if os.path.isfile(db):
        os.remove(db)
    conn = create_connection(db)
    if conn is not None:
        table_CRUD(conn, sql_createTable)
        incomplete = []
        for item in categories:
            try:
                f_bestOfferEnabled = item.getElementsByTagName('BestOfferEnabled')[0].childNodes[0].data
                f_categoryID = item.getElementsByTagName('CategoryID')[0].childNodes[0].data
                f_categoryLevel = item.getElementsByTagName('CategoryLevel')[0].childNodes[0].data
                f_categoryName = item.getElementsByTagName('CategoryName')[0].childNodes[0].data
                f_categoryParentID = item.getElementsByTagName('CategoryParentID')[0].childNodes[0].data
                #print f_categoryID, f_categoryName
            except:
                incomplete.append(item)
        print "INCOMPLETOS MARCADOS:"
        print len(incomplete)
    else:
        print("Error while creating a connection to the database.")
    


    
    

