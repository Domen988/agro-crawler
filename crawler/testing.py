from BeautifulSoup import BeautifulSoup

import urllib2 
url = urllib2.urlopen("http://agromet.mko.gov.si/APP/Tag/Export/262")

content = url.read()

soup = BeautifulSoup(content)

links = soup.findAll("a")

print links

