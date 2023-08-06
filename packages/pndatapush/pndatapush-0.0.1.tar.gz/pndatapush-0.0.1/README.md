# pndatapush
Python module to push data to the Pervasive Nation IoT network. It saves data locally until there is internet access. 

#To install
pip install -r requirements.txt

#To run an example
python gatherdata.py

#To add to your project
Create an instance of the Offline class.

`offline = Offline(payload_consumers=[PNPushData]) #PNPushData is a data consumer class. see pnpushdata.pushdata.PNPushData`

Then when sensor data is received save the data

`offline.save('12456', 30.00) #save(self, deviceid, payload):`