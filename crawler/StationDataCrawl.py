import urllib
import requests
import lxml.html as lh
import re
import os
import datetime

##########################################################################################################
agrometHome = 'http://agromet.mko.gov.si'                                # Naslovi
agrometStations = '/APP/Home/METEO/-1'
exportLink = "/APP/Tag/Export/"             
dataLink = "http://agromet.mko.gov.si/APP/Content/Exports/" 
fileExtensionXML = "60_.xml"                                                 # 30_.xml, 60_.xml, 24_.xml
fileExtensionDAT =  "60_MVal.dat"
subdirectory = "Agrometeo Data"                                           # subdirectory name
##########################################################################################################

try:
    os.mkdir(subdirectory)                                           # use of mkdir: if subd. exists,
except Exception:                                                    # it doesn't do anything
    pass
datList = []
for file in os.listdir(subdirectory):
    if file.endswith(".dat"):
        datList.append(os.path.splitext(file)[0])

print "###############################################################################"
print "Agromet station data crawler"
print "crawls", agrometHome, "and extracts data of all measurements with 1h frequency "
print "all data is saved in subdirectory:", subdirectory
print "################################################################################"
if datList:
    print "Some .dat data allready exists. Script will skip next stations:"
    for ID in datList:
        print ID
else:
    print "No files with ending '.dat' found in project subdirectory", subdirectory

connection = urllib.urlopen(agrometHome + agrometStations)
dom = lh.fromstring(connection.read())
firstLocation = None
first = ""
sessionFlag = False                                                     # session flag for error log creation
for link in dom.xpath('//a/@href'):                                      # select the url in href for all a tags(links)
    if link.startswith(exportLink):                         
        stationID = link.split("/")[-1]

        if stationID in datList:                                             # filter for testing purposes
            continue

        print "Station ID:", stationID
        #print "List of MonthYear options:"
        connectionStation = urllib.urlopen(agrometHome + link)
        domOptions = connectionStation.read().decode("utf8")
        resultOptions = re.findall('<option value="(.*)">', domOptions)   # search for option value using regex, IS THERE ANOTHER WAY?
        #for option in resultOptions:
        #    if option:
        #        print option.encode("utf8")
        print "-------------"

        first = ""

        for option in reversed(resultOptions):
            if option.split(".")[-1] != "2014":                           # exclude all non-2014 data
                continue
            try:
                #if option != "1.2014" and option != "2.2014":             # filter for testing purposes
                #    continue

                payload = {"LocationID": stationID, "MonthYear": option}     # input for form for MonthYear selection

                r = requests.post(agrometHome + link, params=payload)
                result = re.search("/Content/Exports/(.*)" + fileExtensionDAT, r.text)  # search for the right dat file
                if result:
                   #print result.group(1)
                    pass
                else:
                    print "There was no file retrieved from regex search for option:", option
                dataURL = dataLink + result.group(1) + fileExtensionDAT
                urllib.urlretrieve(dataURL, 'temp.dat')

                search = os.listdir('.')
                while dir in search:
                    if dir is 'temp.dat':
                        pass

                fp = open('temp.dat')
                for line in fp.readlines()[1:]:
                    first += line
                fp.close()
                os.remove('temp.dat')
            except:
                print "Option :'", option, "' did not return data."
        ##################################################################################################
        filePath = os.path.join(subdirectory, stationID + ".dat")
        logPath = os.path.join(subdirectory, "ErrorLog.txt")                  # error log file name
        ##################################################################################################
        try:
            if first is not None:
                fp = open(filePath, 'w')
                fp.write(first)
                fp.close()
            else:
                print "Data was not written for station ID:", stationID, "See error log for details."
                fp = open(logPath, "a")                                        # write to error log.txt
                if sessionFlag is False:
                    fp.write(str(datetime.datetime.now()) + "\n")
                    sessionFlag = True
                fp.write(stationID + ".dat was not written." + "\n")
                fp.close()
        except:
            print "Data was not written for station ID:", stationID
if first is "":
    print "-------------"
    print "No files were written."
try:
    os.remove('requests_results.html')
except:
    pass
try:
    os.remove('results.html')

except:
    pass
raw_input("Press Enter to continue...")
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