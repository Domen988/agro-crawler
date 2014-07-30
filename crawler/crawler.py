import urllib
import requests
import lxml.html as lh
import sys
import codecs
import webbrowser
import csv
import re
import xml.etree.ElementTree as ET
from xml.dom.minidom import parse
from cStringIO import StringIO
from lxml import etree
import os
# test line

##########################################################################################################
agrometHome = 'http://agromet.mko.gov.si'                                # Naslovi
agrometStations = '/APP/Home/METEO/-1'
exportLink = "/APP/Tag/Export/"             
dataLink = "http://agromet.mko.gov.si/APP/Content/Exports/" 
fileExtension = "60_.xml"                                                 # 30_.xml, 60_.xml, 24_.xml
subdirectory = "Agrometeo Data"                                           # subdirectory name
##########################################################################################################

try:
    os.mkdir(subdirectory)                                           # use of mkdir: if subd. exists,
except Exception:                                                    # it doesn't do anything
    pass
xmlList = os.listdir(subdirectory)
for file in xmlList:
    file = os.path.splitext(file)[0]
List = [os.path.splitext(file)[0] for file in xmlList]

if List:
    print "Some xml Data allready exists. Script will skip next stations:"
    for ID in List:
        print ID
    print "Location file is not valid!"
    print "------------------------"

connection = urllib.urlopen(agrometHome + agrometStations)
dom =  lh.fromstring(connection.read())
firstLocation = None
for link in dom.xpath('//a/@href'):                                      # select the url in href for all a tags(links)
    if link.startswith(exportLink):                         
        stationID = link.split("/")[-1]

        if stationID in List:                                             # filter for testing purposes
            continue

        print "-------------"
        print "Station ID:", stationID
        #print "List of MonthYear options:"
        connectionStation = urllib.urlopen(agrometHome + link)
        domOptions = connectionStation.read().decode("utf8")
        resultOptions = re.findall('<option value="(.*)">', domOptions)   # search for option value using regex, IS THERE ANOTHER WAY?
        #for option in resultOptions:
        #    if option:
        #        print option.encode("utf8")
        print "-------------"
        ##################################################################################################
        fileName = stationID + ".xml"                                     # file name
        ##################################################################################################

        first = None

        for option in reversed(resultOptions):
            if option.split(".")[-1] != "2014":                           # exclude all non-2014 data
                continue
            try:
                #if option != "1.2014" and option != "2.2014":             # filter for testing purposes
                #    continue

                payload = {"LocationID":stationID,"MonthYear":option}     # input for form for MonthYear selection

                r = requests.post(agrometHome + link, params=payload)
                result = re.search("/Content/Exports/(.*)" + fileExtension, r.text)  # search for the right xml file                       
                if result:
                #    print result.group(1)
                    pass
                else:
                    print "There was no file retrieved from regex search for option:", option
                    pass
                dataURL = dataLink + result.group(1) + fileExtension          
                s = urllib.urlopen(dataURL)
                xmlString = s.read()                                                      # https://docs.python.org/2/library/xml.etree.elementtree.html
                tree = ET.ElementTree(ET.fromstring(xmlString))
                root = tree.getroot()

                for Location in root.findall('Location'):                             # remove 'Location' header. No important info in there
                    root.remove(Location)

                if first is None:                                            # creates xml or extends existing
                    first = root                                             #
                else:                                                        #
                    first.extend(root)                                       #

            except:
                print "Option :'", option, "' did not return data."
        ##################################################################################################
        file= stationID + ".xml"                                             # file name
        path=os.path.join(subdirectory, file)
        logPath = os.path.join(subdirectory, "ErrorLog.txt")                  # error log file name
        ##################################################################################################
        try:
            if first is not None:
                fp=open(path,'w')
                tree = ET.ElementTree(first)
                tree.write(fp)
                fp.close()
            else:
                print "Data was not written for station ID:", stationID
                fp = open(logPath, "a")                                        # write to error log.txt
                fp.write(stationID + ".xml was not written." + "\n")
                fp.close()
        except:
            print "Data was not written for station ID:", stationID


        """

        #
        # Next piece of code collects location data in 'Location.xml'. It saves in same subdirectory as for meteo data.
        try:
            s = urllib.urlopen(dataURL)
            xmlString = s.read()                                                      
            tree = ET.ElementTree(ET.fromstring(xmlString))
            root = tree.getroot()

            for DATA in root.findall('DATA'):                             # remove 'DATA', so that 'Location' element stays
                root.remove(DATA)
               
            if firstLocation is None:                                     # creates xml or extends existing
                firstLocation = root                                      #
            else:                                                         #
                firstLocation.extend(root)                                #
        except:
            print "Problems with location file."
##################################################################################################
file= "Location" + ".xml"                                             # file name
path=os.path.join(subdirectory, file)
##################################################################################################
try:
    fp=open(path,'w');
    tree = ET.ElementTree(firstLocation)
    tree.write(fp, encoding="UTF-8")
    fp.close()
except:
    print "Location data could not be written."

"""