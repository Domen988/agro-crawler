
import time
from selenium.webdriver import Firefox
import os
import re
from GaussKruegerToWGS import convert_GK_to_lat_long
##########################################################################################
gis_url = 'http://gis.furs.gov.si/pregl/#config=AGMET.xml&query=AG_POSTAJE_METEO_TEMP:entCode:'
subdirectory = "Agrometeo Data"
##########################################################################################
print "###############################################################################"
print "FURS location crawler"
print "crawls FURS with station ID's from subdirectory ", subdirectory, ". Gets coordinates"
print 'in Gaus-Krueger coordinate system. Transforms to WGS 84 cs. Saves to a CSV file.'
print "all data is saved in subdirectory:", subdirectory
print "################################################################################"

datList = []
for file in os.listdir(subdirectory):
    if file.endswith(".dat"):
        datList.append(os.path.splitext(file)[0])

datList = [int(x) for x in datList]
datList.sort()
stationGEO = []

for station_ID in datList:
    print station_ID
    #if station_ID is not 255 and station_ID is not 2:
    #    continue
    url = gis_url + str(station_ID)
    driver = Firefox()
    driver.get(url)
    time.sleep(12)
    full_url = driver.current_url
    driver.close()
    stationX_GK = float((re.search("map_x=(.*?)&", full_url)).group(1))
    stationY_GK = float((re.search("map_y=(.*?)&", full_url)).group(1))

    stationX_WGS, stationY_WGS = convert_GK_to_lat_long(stationX_GK, stationY_GK)

    stationGEO.append((station_ID, stationX_WGS, stationY_WGS))

filePath = os.path.join(subdirectory, "stations_Geo_location.txt")                  # error log file name
open(filePath, 'w').write('\n'.join('%s, %s, %s' % x for x in stationGEO))
