from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SensorData(Base):
	__tablename__ = 'sensordata'

	id = Column(Integer, Sequence('data_id_seq'), primary_key=True)
	timestamp = Column(Text, nullable=False)
	deviceid = Column(String, index=True, nullable=False)
	payload = Column(String, nullable=False)
	sent = Column(Boolean, index=True, default=False)

	def __repr__(self):
		return "<SensorData(deviceid='%s', timestamp='%s', payload='%s', sent='%s')>" % (self.deviceid, self.timestamp, self.payload, self.sent)
