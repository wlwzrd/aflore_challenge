import httplib

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


def setHeaders():
    """ Create headers for API call
    :return: created headers with Ebay API information
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
    return headers

def setRequest():
    """ Create request info for API call
    :return: created data request
    """
    xmlIn = "<?xml version='1.0' encoding='utf-8'?>"+\
            "<GetCategoriesRequest xmlns='urn:ebay:apis:eBLBaseComponents'>"+\
            "<RequesterCredentials>"+\
            "<eBayAuthToken>" + g_unsignedToken + "</eBayAuthToken>"+\
            "</RequesterCredentials>"+\
            "<CategorySiteID>" + g_SiteID.encode("utf-8")  + "</CategorySiteID>"+\
            "<DetailLevel>ReturnAll</DetailLevel>"+\
            "</GetCategoriesRequest>"
    return xmlIn

def getEbayXml():
    """Connects to the Ebay API
    :return: xml response from the API call
    """
    headers = setHeaders()
    xmlIn = setRequest()
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
