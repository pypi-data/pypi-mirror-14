from datetime import datetime
from sensordata import SensorData, Base
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import os
from threading import Thread
import urllib2
import time

def active_internet_connection():
	try:
		#85.91.7.19 is one of the IP-addresses for google.ie
		response=urllib2.urlopen('http://85.91.7.19', timeout=1)
		return True
	except urllib2.URLError as err: pass
	return False


class Offline(object):
	session = null
	engine = null
	payload_consumers = []

	def __init__(self, payload_consumers = []):
		self.payload_consumers = payload_consumers
		self.engine = create_engine('sqlite:///%s/sensordata.db' % os.path.dirname(os.path.realpath(__file__)), echo=False)
		self.Session = sessionmaker(bind=self.engine)
		self.session = self.Session()
		# Create the database if it doesn't exist
		Base.metadata.create_all(self.engine,  checkfirst=True)

		# start a thread that loops through all unsent messages and pushes to all configured consumers
		thread = Thread(target = self.push_unsent_payloads)
		thread.daemon = True
		thread.start()

	def save(self, deviceid, payload):
		payloadobj = SensorData(deviceid=str(deviceid), timestamp=str(datetime.utcnow()), payload=str(payload), sent=False)
		self.session.add(payloadobj)
		self.session.commit()

	def push_unsent_payloads(self):
		#we need to create our own session here as we're running in a new thread
		local_session = self.Session()
		while True:
			# check if internet access
			if active_internet_connection():
				for payload in local_session.query(SensorData).filter_by(sent=False):
					#print('Pushing [%d] %s (%s) to all consumers' % (payload.id, str(payload.payload), str(payload.timestamp)))
					for consumer in self.payload_consumers:
						consumer_obj = consumer()
						consumer_obj.push(payload.deviceid, payload.timestamp, payload.payload)
						payload.sent = True
						local_session.commit()


