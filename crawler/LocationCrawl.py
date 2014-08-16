
import time
from selenium.webdriver import Firefox
import os
import re
from GaussKruegerToWGS import convert_GK_to_lat_long
##########################################################################################
gis_url = 'http://gis.furs.gov.si/pregl/#config=AGMET.xml&map_x=0&map_y=0&map_sc=3571&query=AG_POSTAJE_METEO_TEMP:entCode:'
subdirectory = "Agrometeo Data"
fileName = "stations_Geo_location.txt"
errorFileName = "LocationErrorLog.txt"
##########################################################################################

print "....................................................................................."
print "FURS location crawler"
print "crawls FURS with station ID's from subdirectory ", subdirectory, ". Gets coordinates"
print 'in Gaus-Krueger coordinate system. Transforms to WGS 84 cs. Saves to a CSV file.'
print "all data is saved in subdirectory:", subdirectory
print "....................................................................................."

filePath = os.path.join(subdirectory, fileName)
errorFilePath = os.path.join(subdirectory, errorFileName)

stationDoneList = []
if os.path.isfile(filePath):
    fp = open(filePath, 'r')
    allreadyDoneLines = fp.readlines()
    fp.close()
    for line in allreadyDoneLines:
        stationIDdone = int(line.split(",")[0])
        stationDoneList.append(stationIDdone)

    print "Next stations locations are allready colected:"
    print stationDoneList
    print "Collection will continue on remaining stations."

datList = []
for file in os.listdir(subdirectory):
    if file.endswith(".dat"):
        datList.append(os.path.splitext(file)[0])

datList = [int(x) for x in datList]
datList.sort()

stationGEO = []
stationsWithErrors = []

for station_ID in datList:
    if station_ID in stationDoneList:
        continue
    print station_ID
    #if station_ID is not 255 and station_ID is not 2:
    #    continue
    try:
        url = gis_url + str(station_ID)
        driver = Firefox()
        driver.get(url)
        time.sleep(8)
        full_url = driver.current_url
        driver.close()
        stationX_GK = float((re.search("map_x=(.*?)&", full_url)).group(1))
        stationY_GK = float((re.search("map_y=(.*?)&", full_url)).group(1))

        #stationX_WGS, stationY_WGS = convert_GK_to_lat_long(stationX_GK, stationY_GK)
        stationX_WGS, stationY_WGS = stationX_GK, stationY_GK
        #stationGEO = []

        #stationGEO.append((station_ID, stationX_WGS, stationY_WGS))

        fp = open(filePath, 'a')
        #fp.write('\n'.join('%s, %s, %s' % x for x in stationGEO))
        a = (station_ID, stationX_WGS, stationY_WGS)
        print a
        fp.write('\n' + ', '.join(str(i) for i in a))
        fp.close()
    except:
        print "something not ok with station:", station_ID
        fp = open(errorFileName, 'a')
        fp.write(str(station_ID))
        fp.close()




