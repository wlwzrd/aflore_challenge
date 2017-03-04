import os
import sys
import getopt
 
from xml.dom.minidom import parse, parseString
from ebayHelper import getEbayXml
from sqlHelper import createConnection, runSQL, DB_name, SQL_createTable, insertSQL

__author__ = "Mario Gutierrez/wlwzrd"
__email__ = "mfdogutierrez@gmail.com"

def build():
    xmlOut = getEbayXml()
    response = parseString(xmlOut)
    categories = response.getElementsByTagName('Category')
    # categories[numero de categorias].childNodes[0..5].childNodes[0].data
    if os.path.isfile(DB_name):
        os.remove(DB_name)
    conn = createConnection(DB_name)
    if conn is not None:
        status = runSQL(conn, SQL_createTable)
        if status:
            incomplete = []
            success = 0
            fails = 0
            for item in categories:
                try:
                    f_bestOfferEnabled = (item.getElementsByTagName('BestOfferEnabled')[0].childNodes[0].data).encode('utf-8')
                    f_categoryID = (item.getElementsByTagName('CategoryID')[0].childNodes[0].data).encode('utf-8')
                    f_categoryLevel = (item.getElementsByTagName('CategoryLevel')[0].childNodes[0].data).encode('utf-8')
                    f_categoryName = (item.getElementsByTagName('CategoryName')[0].childNodes[0].data).encode('utf-8')
                    f_categoryParentID = (item.getElementsByTagName('CategoryParentID')[0].childNodes[0].data).encode('utf-8')
                    insert = runSQL(conn, insertSQL(f_categoryID,f_categoryName,f_categoryLevel,f_bestOfferEnabled,f_categoryParentID))
                    if insert:
                        success += 1
                    else:
                        fails += 1
                except:
                    incomplete.append({"Category ID":f_categoryID})
            print "DATABASE SUCCESSFULLY CREATED!"
            print "---------------------------------"
            print "Success Insertions: ", success
            print "Fail Insertions: ", fails
            print "Incomplete Categories: ", len(incomplete) 
            print "---------------------------------"
            return True
        else: 
            print "Can't create table..."
    else:
        print("Error while creating a connection to the database.")

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
            print "BUILDIND DATABASE FROM EBAY API..."
            build()
        elif opt  == '--render':
            category_id = arg
            print "CAtegoria buscada: ", category_id

if __name__ == "__main__":
    main(sys.argv[1:])

    
    

