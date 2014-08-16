
import GaussKruegerToWGS

right = 596953.75
height = 91624
right += 0
height += 0

r1, y1, = GaussKruegerToWGS.convert_GK_to_lat_long(right, height, use_wgs84=None)
print r1, y1
"""

import time
from selenium.webdriver import Firefox # pip install selenium

gis_url = 'http://gis.furs.gov.si/pregl/#config=AGMET.xml&query=AG_POSTAJE_METEO_TEMP:entCode:'
station_ID = '16'
url = gis_url + station_ID
# use firefox to get page with javascript generated content

driver = Firefox()
driver.get(url)
time.sleep(15)
print driver.current_url
"""
