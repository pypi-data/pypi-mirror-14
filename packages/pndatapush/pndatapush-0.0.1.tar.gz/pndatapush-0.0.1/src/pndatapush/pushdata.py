from abc import ABCMeta, abstractmethod


class PushDataBase(object):
	__metaclass__=ABCMeta

	# TODO - add property 'name' for use with logging

	# TODO - add property on whether or not to check if push was successful before marking as sent

	# TODO - add abstract method for checking whether the push was successful.

	@abstractmethod
	def push(self, deviceid, timestamp, payload):
		pass


class PNPushData(PushDataBase):

	def push(self, deviceid, timestamp, payload):
		print('Pushing %s data to PN %s with timestamp %s' % (str(deviceid), str(payload), str(timestamp)))
