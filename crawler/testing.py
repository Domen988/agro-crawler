from BeautifulSoup import BeautifulSoup
import os
import urllib2 
url = urllib2.urlopen("http://agromet.mko.gov.si/APP/Tag/Export/262")



subdirectory = "Agrometeo Data"                                           # subdirectory name
xmlList = os.listdir(subdirectory)
for file in xmlList:
    filePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), subdirectory, file)
    if os.stat(filePath)[6]==0:
        os.remove(filePath)
        print "%s deleted", file
    else:
        pass
