# *****************************************************************************
# Copyright (c) 2016 Adam Milton-Barker - TechBubble Technologies and other Contributors.
#
# The MIT License (MIT)
#
# Copyright (c) 2016 AdamMiltonBarker
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Contributors:
#   Adam Milton-Barker  - Initial Contribution
#   Adam Mosely  - Tester
# *****************************************************************************

import inspect
import json
import os
import paho.mqtt.client as mqtt
import sys
import time

class JumpWayDeviceConnection():
	
	def __init__(self, configs):	
		self._configs = configs
		self.mqttClient = None
		self.mqttTLS =  os.path.dirname(os.path.abspath(__file__)) + "/ca.pem"
		self.mqttHost = 'iot.techbubbletechnologies.com'
		self.mqttPort = 8883	
		self.deviceStatusCallback = None	
		self.deviceSensorCallback = None
		self.deviceMessageCallback = None
		if self._configs['locationName'] == None:
			raise ConfigurationException("locationName property is required")
		if self._configs['zoneID'] == None:
			raise ConfigurationException("zoneID property is required")
		elif self._configs['deviceId'] == None:
			raise ConfigurationException("deviceId property is required")
		elif self._configs['username'] == None: 
			raise ConfigurationException("username property is required")
		elif self._configs['password'] == None: 
			raise ConfigurationException("password property is required")
	
	
	def connectToDevice(self):
		self.mqttClient = mqtt.Client(client_id=self._configs['locationName'], clean_session=False)
		self.mqttClient.tls_set(self.mqttTLS, certfile=None, keyfile=None)
		self.mqttClient.on_connect = self.on_connect
		self.mqttClient.on_message = self.on_message
		self.mqttClient.on_publish = self.on_publish
		self.mqttClient.on_subscribe = self.on_subscribe
		#self.mqttClient.on_log = self.on_log
		self.mqttClient.username_pw_set(str(self._configs['username']),str(self._configs['password']))
		self.mqttClient.connect(self.mqttHost,self.mqttPort,10)
		self.mqttClient.loop_start()

	def on_connect(self, client, obj, flags, rc):
			self.publishToDeviceStatus({"STATUS":"ONLINE"})
			print("rc: "+str(rc))
	
	def subscribeToDeviceStatus(self, qos=0):
		if self._configs['locationName'] == None:
			print("locationName is required!")
		elif self._configs['username'] == None:
			print("username is required!")
			return False
		elif self._configs['zoneID'] == None:
			print("zoneID is required!")
			return False
		elif self._configs['deviceId'] == None:
			print("deviceId is required!")
			return False
		else:
			deviceStatusTopic = '%s/Devices/%s/%s/Status' % (self._configs['locationName'], self._configs['zoneID'], self._configs['deviceId'])
			self.mqttClient.subscribe(deviceStatusTopic, qos=qos)
			return True
	
	def subscribeToDeviceMessages(self, qos=0):
		if self._configs['locationName'] == None:
			print("locationName is required!")
		elif self._configs['username'] == None:
			print("username is required!")
			return False
		elif self._configs['zoneID'] == None:
			print("zoneID is required!")
			return False
		elif self._configs['deviceId'] == None:
			print("deviceId is required!")
			return False
		else:
			deviceMessageTopic = '%s/Devices/%s/%s/Messages' % (self._configs['locationName'], self._configs['zoneID'], self._configs['deviceId'])
			self.mqttClient.subscribe(deviceMessageTopic, qos=qos)
			return True
	
	def subscribeToDeviceSensors(self, qos=0):
		if self._configs['locationName'] == None:
			print("locationName is required!")
			return False
		elif self._configs['username'] == None:
			print("username is required!")
			return False
		elif self._configs['zoneID'] == None:
			print("zoneID is required!")
			return False
		elif self._configs['deviceId'] == None:
			print("deviceId is required!")
			return False
		else:
			deviceDataTopic = '%s/Devices/%s/%s/Sensors' % (self._configs['locationName'], self._configs['zoneID'], self._configs['deviceId'])
			self.mqttClient.subscribe(deviceDataTopic, qos=qos)
			return True

	def on_subscribe(self, client, obj, mid, granted_qos):
			print("Subscribed: "+str(self._configs['locationName']))

	def on_message(self, client, obj, msg):
		splitTopic=msg.topic.split("/")
		if splitTopic[3]=='Status':
			if self.deviceStatusCallback == None:
				print("No deviceStatusCallback set")
			else:
				self.deviceStatusCallback(msg.topic,msg.payload)
		elif splitTopic[3]=='Sensors':
			if self.deviceSensorCallback == None:
				print("No deviceSensorCallback set")
			else:
				self.deviceSensorCallback(msg.topic,msg.payload)
		elif splitTopic[3]=='Message':
			if self.deviceMessageCallback == None:
				print("No deviceMessageCallback set")
			else:
				self.deviceMessageCallback(msg.topic,msg.payload)
		print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
	
	def publishToDeviceStatus(self, data):
		if self._configs['locationName'] == None:
			print("locationName is required!")
		elif self._configs['username'] == None:
			print("username is required!")
			return False
		elif self._configs['zoneID'] == None:
			print("zoneID is required!")
			return False
		elif self._configs['deviceId'] == None:
			print("deviceId is required!")
			return False
		else:
			deviceStatusTopic = '%s/Devices/%s/%s/Status' % (self._configs['locationName'], self._configs['zoneID'], self._configs['deviceId'])
			self.mqttClient.publish(deviceStatusTopic,json.dumps(data))
	
	def publishToDeviceMessages(self, data):
		if self._configs['locationName'] == None:
			print("locationName is required!")
		elif self._configs['username'] == None:
			print("username is required!")
			return False
		elif self._configs['zoneID'] == None:
			print("zoneID is required!")
			return False
		elif self._configs['deviceId'] == None:
			print("deviceId is required!")
			return False
		else:
			deviceMessagesTopic = '%s/Devices/%s/%s/Messages' % (self._configs['locationName'], self._configs['zoneID'], self._configs['deviceId'])
			self.mqttClient.publish(deviceMessagesTopic,json.dumps(data))
	
	def publishToDeviceSensors(self, data):
		if self._configs['locationName'] == None:
			print("locationName is required!")
		elif self._configs['username'] == None:
			print("username is required!")
			return False
		elif self._configs['zoneID'] == None:
			print("zoneID is required!")
			return False
		elif self._configs['deviceId'] == None:
			print("deviceId is required!")
			return False
		else:
			deviceSensorsTopic = '%s/Devices/%s/%s/Sensors' % (self._configs['locationName'], self._configs['zoneID'], self._configs['deviceId'])
			self.mqttClient.publish(deviceSensorsTopic,json.dumps(data))

	def on_publish(self, client, obj, mid):
			print("Published: "+str(mid))

	def on_log(self, client, obj, level, string):
			print(string)
	
	def disconnectFromDevice(self):
		self.publishToDeviceStatus({"STATUS":"OFFLINE"})
		self.mqttClient.disconnect()	
	
			
