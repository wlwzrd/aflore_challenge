import os
import sys
import getopt
 
from xml.dom.minidom import parse, parseString
from ebayHelper import getEbayXml
from sqlHelper import createConnection, runSQL, DB_name, SQL_createNestedTable, SQL_falseParent, insertNode, countSQL,getCategories

__author__ = "Mario Gutierrez/wlwzrd"
__email__ = "mfdogutierrez@gmail.com"

def sortCategoriesByLevel(categoriesXml):
    categoriesList =[]
    for item in categoriesXml:
        try:
            f_bestOfferEnabled = (item.getElementsByTagName('BestOfferEnabled')[0].childNodes[0].data).encode('utf-8')
            f_categoryID = (item.getElementsByTagName('CategoryID')[0].childNodes[0].data).encode('utf-8')
            f_categoryLevel = (item.getElementsByTagName('CategoryLevel')[0].childNodes[0].data).encode('utf-8')
            f_categoryName = (item.getElementsByTagName('CategoryName')[0].childNodes[0].data).encode('utf-8')
            f_categoryParentID = (item.getElementsByTagName('CategoryParentID')[0].childNodes[0].data).encode('utf-8')
            categoriesList.append({"bOE":f_bestOfferEnabled,"cID":f_categoryID,"cLevel":f_categoryLevel,"cName":f_categoryName,"cParentID":f_categoryParentID})
        except Exception,err:
            print "CATEGORIES.PY:", err,  item.getElementsByTagName('CategoryID')[0].childNodes[0].data
    categoriesOrdered = sorted(categoriesList, key = lambda cat: (cat['cLevel']))
    return categoriesOrdered

def genJson(rows):
    data = {"categoryID":"100548", "categoryName":"Toys", "tree": {"name":"Hello","children":[{"name":"Child 1"},{"name":"Child 2"}]}}
    categoriesList = [] 
    for row in rows:
        j_cID = row[0]
        j_cName = row[1]
        j_cLevel = row[2]
        j_cParentID = row[3]
        categoriesList.append({"cID":j_cID,"cName":j_cName,"cLevel":j_cLevel,"cParentID":j_cParentID})
    categoriesOrdered = sorted(categoriesList, key = lambda cat: (cat['cLevel']))
    
    

def build():
    xmlOut = getEbayXml()
    response = parseString(xmlOut)
    categories = response.getElementsByTagName('Category')
    categoriesOrdered = sortCategoriesByLevel(categories)
    if os.path.isfile(DB_name):
        os.remove(DB_name)
    conn = createConnection(DB_name)    
    if conn is not None:
        runSQL(conn, SQL_createNestedTable)
        runSQL(conn, SQL_falseParent)
        for itemO in categoriesOrdered:
            try:
                insertNode(conn, itemO["cID"],itemO["cName"],itemO["cLevel"],itemO["bOE"],itemO["cParentID"])
            except Exception,err:
                print "INSERT:", err, itemO["cID"]
        c = countSQL(conn)
        print "---------------------------------"
        print "Database Successfully Created!"
        print "Created: ", c
        print "---------------------------------"
    else:
        print("Error while creating a connection to the database.")

def createData(categoryID):
    if os.path.isfile(DB_name):
        conn = createConnection(DB_name)
        if conn is not None:
            algo = getCategories(conn,categoryID)
            for item in algo:
                print item[0],item[1],item[2]
            print "GENERATED"
            #algo2 = genJson(algo)
            #createHtml()
            #createJs(algo2)
        else:
            #No se puedo establecer conexion
            print("Error while creating a connection to the database.")
    else:
        #NO hay BAse de datos
        print("FATAL: Seens like there is not a database.")

         
def main(argv):
    category_id = ""
    try:
        opts, args =getopt.getopt(argv, "h", ["rebuild","render="])
    except getopt.GetoptError:
        print " --rebuild / --render <category_id>"
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print './categories --rebuild / --render <category_id>'
            sys.exit()
        elif opt == '--rebuild':
            print "Just wait a momment, something magical is happening in the database..."
            build()
        elif opt  == '--render':
            category_id = arg
            print "Categoria buscada: ", category_id
            createData(category_id)

if __name__ == "__main__":
    main(sys.argv[1:])

    
    

