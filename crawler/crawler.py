import urllib
import requests
import lxml.html as lh
import sys
import codecs
import webbrowser

sys.stdout = codecs.getwriter('utf8')(sys.stdout)



agrometHome = 'http://agromet.mko.gov.si'
agrometStations = '/APP/Home/METEO/-1'
connection = urllib.urlopen(agrometHome + agrometStations)

dom =  lh.fromstring(connection.read())

for link in dom.xpath('//a/@href'):                                    # select the url in href for all a tags(links)
    #print link
    if link == "/APP/Tag/Export/262":                            # test 19,2
        print link
        print "-----"
        stationLink = link
        conStation = urllib.urlopen(agrometHome + stationLink)

        domStation = lh.fromstring(conStation.read())

        for link in domStation.xpath('//a/@href'):
            print link

        payload = {"LocationID":"262","LocationName":"Arti?e","DeviceCode":"42800","MonthYear":"6.2014"}
        r = requests.post(agrometHome + stationLink, params=payload)
        print r.text

          ##  Kaj pravi Jasna:
          ##  treba bo iskat po r.text z regex ali pythonovimi string metodami.
          ##  elegantneje ne bo slo, ker tip uporablja ajax(-e ?). Request ne vrne novega url-ja, pac pa na isti url nalozi novo vsebino


        print "---"
        ret = dir(r)
        print ret
        print "'''"
        print r.links
        print r.url

        print "w'''"

        ####################
        #from BeautifulSoup import BeautifulSoup
        #
        #import urllib2 
        #
        #
        #soup = BeautifulSoup(r.text)
        #
        #links = soup.findAll("a")
        #
        #print links
        ###################################
        #domData = lh.fromstring(f.read())
        #for link in domData.xpath('//a/@href'):
        #    print link
        #    
        
        #print(r.decode('utf-8').encode('cp850','replace').decode('cp850'))
 

        #print r


        #webbrowser.open(agrometHome + stationLink)


    """
for element, attribute, link, pos in dom.iterlinks():
    if link[0:19] == "/APP/Detail/METEO/2":
        print "----"
        print "ele", element
        print "att", attribute
        print "lnk", link
        print "pos", pos
        """