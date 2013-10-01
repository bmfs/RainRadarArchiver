import urllib2
import time
import os

def getLastImage():
	request = urllib2.Request('http://www.weather.gov.sg/wip/pp/rndops/web/ship/gif/rad70.gif')
	opener = urllib2.build_opener()
	firstdatastream = opener.open(request)
	
	last_modified = time.strptime(firstdatastream.headers.dict['last-modified'], "%a, %d %b %Y %H:%M:%S %Z")

	minutes = (int(last_modified.tm_min)/5)*5
	minutes = "%s%s" % ( ('0' if minutes<10  else ''), minutes)
	hour = time.strftime("%H", last_modified)
	day = time.strftime("%d",last_modified)
	month = time.strftime("%m",last_modified)
	print minutes, hour, day, month

	radar_time = "%s%s" % (hour, minutes)

	image_path = os.path.join(os.getcwd(), 'archive', str(last_modified.tm_year), month, day, "%s.gif" % radar_time)

	if (checkIfExists(image_path)):
		pass
	else:
		#make sure directory exists
		createDirectory(str(last_modified.tm_year), month, day )

		try:
			f = open(image_path, 'wb')
			f.write(firstdatastream.read())
			f.close()
		except IOError,e:
			print e
		#download file

def createDirectory(year, month, day):
	year_path = os.path.join(os.getcwd(), 'archive', year)
	month_path = os.path.join(os.getcwd(), 'archive', year, month)
	day_path = os.path.join(os.getcwd(), 'archive', year, month, day)
	try:
		if (not os.path.isdir(day_path)):
			os.makedirs(day_path) 
	except IOError,e:
		print e
	else:
		print "Successful"

def checkIfExists(path):
	try:
   		with open(path): pass
   		return True
	except IOError:
   		return False

getLastImage()