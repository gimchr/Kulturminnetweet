#!/usr/bin/env python
# -*- coding: iso-8859-10 -*-

from twython import Twython
import urllib2, json, random

APP_KEY = 'insert'
APP_SECRET = 'insert'
OAUTH_TOKEN = 'insert'
OAUTH_TOKEN_SECRET = 'insert'

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

result = None

while result is None:
	try:
		kulturminne = urllib2.urlopen("http://askeladden_wms.ra.no/arcgis/rest/services/WMS/RA_Askeladden/MapServer/5/query?where=LokalitetID+=+" + str(random.randrange(2900,181200)) + "&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&f=json")
		kulturminneValues = json.load(kulturminne)
		kulturminne.close()
		KOMM = str(kulturminneValues['features'][0]['attributes']['KOMM'])
		break
	except:
		pass
		
if len(KOMM) == 4:
	kommunenummer = urllib2.urlopen("http://hotell.difi.no/api/json/ssb/regioner/kommuner?query=" + KOMM)
else:
	kommunenummer = urllib2.urlopen("http://hotell.difi.no/api/json/ssb/regioner/kommuner?query=0" + KOMM)
kommunenummerValues = json.load(kommunenummer)
kommunenummer.close()

tweetNavn = kulturminneValues['features'][0]['attributes']['Navn']
tweetKOMM = kommunenummerValues['entries'][0]['tittel']
vernetypeID = kulturminneValues['features'][0]['attributes']['VernetypeID']

translations = { 'AUT': 'er #automatisk #fredet',
'VED': 'er #vedtaksfredet',
'FOR': 'er #forskriftsfredet',
'FRE': 'er #fredet',
'MID': 'er #midlertidig #fredet',
'FPG': 'er under #fredning',
'PBL': 'er #vernet etter #PBL',
'KMV': 'er #kommunalt #verneverdig',
'LIST': 'er en #listeført #kirke',
'STAT': 'er #statlig #listeført',
'KOM': 'er #kommunalt #listeført',
'UAV': 'har #uavklart #vernestatus',
'OPP': 'er en #opphevet #fredning',
'FJE': 'er #fjernet',
'IKKE': 'er #ikke #fredet',
'SAM': 'har #sammensatt #vernestatus'
}

try:
	vernetypeTrans = translations[vernetypeID]
except:
	vernetypeTrans = vernetypeID

try:
	bilde = urllib2.urlopen("http://kulturminnebilder.ra.no//fotoweb/cmdrequest/rest/PreviewAgent.fwx?ar=5001&sr=" + str(kulturminneValues['features'][0]['attributes']['LokalitetID']))
except IOError:
	bilde = None
	
tweet = "#" + tweetNavn + " i #" + tweetKOMM + " kommune " + vernetypeTrans + " (http://www.kulturminnesok.no/ra/lokalitet/" + str(kulturminneValues['features'][0]['attributes']['LokalitetID']) + ")"

if bilde != None:	
	twitterbilde = twitter.upload_media(media=bilde)	
	twitter.update_status(status=tweet, media_ids=[twitterbilde['media_id']])
else:
	twitter.update_status(status=tweet)
