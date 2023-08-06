import random
import decimal
from helpers import prompt
from pndatapush.offline import Offline
from pndatapush.pushdata import PNPushData


def gen_random_decimal(i, d):
	return decimal.Decimal('%d.%d' % (random.randint(0,i),random.randint(0,d)))


def wait_for_data():
	offline = Offline(payload_consumers=[PNPushData])
	while True:
		sensor_payload = prompt('Enter Sensor Data', default=gen_random_decimal(35,99))
		print('Pushing %s to your AEP of choice ' % str(sensor_payload))
		offline.save('123456',sensor_payload)

if __name__ == '__main__':
	print('Gather data from console - random defaults are provided')
	wait_for_data()
