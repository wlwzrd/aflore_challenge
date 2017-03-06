import os
import sys
import getopt
 
from xml.dom.minidom import parse, parseString
from ebayHelper import getEbayXml
from sqlHelper import createConnection, runSQL, DB_name, SQL_createNestedTable, SQL_falseParent, insertNode, countSQL,getCategories
from webHelper import createHTML, createJS
__author__ = "Mario Gutierrez/wlwzrd"
__email__ = "mfdogutierrez@gmail.com"

def sortCategoriesByLevel(categoriesXml):
    """ Sort a list of categories(sort list of dict by a key)
    :param:categoriesXml: String XML
    :return: List of dicts ordered by Category Level
    """
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

def genTree(categoriesOrdered,parentNode):
    """ Generate Hierarchical Tree
    """
    filterList = [parentNode["cID"]]
    result = [d for d in categoriesOrdered if d["cParentID"] in filterList]
    if len(result)>0:
        #HIJOS
        children = []
        for j in result:
            l = genTree(categoriesOrdered,j)
            children.append(l)
        return {"name":parentNode["cName"],"children":children}
    else:
        return {"name":parentNode["cName"]}
        

def genJson(rows):
    """ Generate a Json Schema (Python dict)
    :param:rows: sql fech from the data by Category ID
    :return: Dict representing the hierarchical tree of a category
    """
    data = {"categoryID":"100548", "categoryName":"Toys", "tree": {"name":"Hello","children":[{"name":"Child 1"},{"name":"Child 2"}]}}
    categoriesList = [] 
    for row in rows:
        j_cID = row[0]
        j_cName = row[1]
        j_cLevel = row[2]
        j_cParentID = row[3]
        categoriesList.append({"cID":j_cID,"cName":j_cName,"cLevel":j_cLevel,"cParentID":j_cParentID})
    categoriesOrdered = sorted(categoriesList, key = lambda cat: (cat['cLevel']))
    parentNode = categoriesOrdered[0]
    tree = genTree(categoriesOrdered,parentNode)
    data = {"categoryID":parentNode["cID"], "categoryName":parentNode["cName"], "tree":tree}
    return data
    

def build():
    """ Create the database based on the Ebay categories using Ebay API
    """
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
        #c = countSQL(conn)
        print "---------------------------------"
        print "Database Successfully Created!"
        #print "Created: ", c
        #print "---------------------------------"
    else:
        print("Error while creating a connection to the database.")

def createData(categoryID):
    if os.path.isfile(DB_name):
        conn = createConnection(DB_name)
        if conn is not None:
            selectCategories = getCategories(conn,categoryID)
            dataJson = genJson(selectCategories)
            createHTML(categoryID)
            createJS(dataJson)
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
            #print "Categoria buscada: ", category_id
            createData(category_id)

if __name__ == "__main__":
    main(sys.argv[1:])

    
    

