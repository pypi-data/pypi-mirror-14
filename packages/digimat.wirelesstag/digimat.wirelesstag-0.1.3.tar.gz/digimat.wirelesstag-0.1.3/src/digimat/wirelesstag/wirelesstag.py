import time
import pprint
import json

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import logging, logging.handlers

# API documentation here
# http://wirelesstag.net/media/mytaglist.com/apidoc.html

WIRELESSTAG_API_URL='https://www.mytaglist.com'


class WirelessDataObject(object):
	def __init__(self, data):
		self._data={}
		self._stamp=0
		self.onInit()
		self.update(data)

	def onInit(self):
		pass

	def validateData(self, data):
		return True

	def update(self, data):
		if data:
			try:
				if self.validateData(data):
					self._data=data
					self._stamp=time.time()
			except:
				pass

	def get(self, name, default=None):
		try:
			return self._data[name]
		except:
			return default

	def __getitem__(self, name):
		return self.get(name)

	def age(self):
		return time.time()-self._stamp

	def stampLastCommunication(self):
		return int(self.get('lastComm', 0))

	def dump(self):
		pprint.pprint(self._data)

	def idstr(self):
		return ''

	def __repr__(self):
		return '%s(%s)' % (type(self).__name__, self.idstr())


class Manager(WirelessDataObject):
	def __init__(self, channel, data):
		super(Manager, self).__init__(data)
		self._channel=channel

	@property
	def channel(self):
	    return self._channel

	@property
	def logger(self):
		return self.channel.logger
	
	def onInit(self):
		self._tags={}
		self._tagsIndexByName={}
		self._selected=False

	def idstr(self):
		try:
			return '%s/%s' % (self.mac, self.name)
		except:
			return ''

	def validateData(self, data):
		try:
			mac=data['mac']
			if mac and (self.mac is None or self.mac==mac):
				return True
		except:
			pass

	@property
	def mac(self):
	    return self.get('mac')

	@property
	def name(self):
	    return self.get('name')

	def unselect(self):
		self._selected=False

	def select(self, force=False):
		if force or not self._selected:
			# mark all managers as unselected (no order sent for this), just a flag reset
			for manager in self.channel.managers():
				manager.unselect()

			if self.mac is not None:
				if self.channel.do(self.channel.apiEthAccount('SelectTagManager'), {'mac': self.mac}):
					self._selected=True
		return self._selected

	def retrieveTags(self):
		if self.select():
			return self.channel.doAndGetData(self.channel.apiEthClient('GetTagList'))

	def tags(self):
		try:
			return self._tags.values()
		except:
			pass

	def tag(self, uuid):
		try:
			return self._tags[uuid]
		except:
			pass

	def tagFromName(self, name):
		try:
			return self._tagsIndexByName[name]
		except:
			pass

	def __getitem__(self, name):
		return self.tagFromName(name)

	def tagStore(self, data):
		try:
			uuid=data['uuid']
			if uuid:
				tag=self.tag(uuid)
				if tag:
					tag.update(data)
				else:
					tag=Tag(self, data)
					self._tags[tag.uuid]=tag
					if tag.name:
						self._tagsIndexByName[tag.name]=tag
				return tag
		except:
			pass

	def read(self):
		tags=self.retrieveTags()
		if tags:
			for data in tags:
				self.tagStore(data)
			return True


class Tag(WirelessDataObject):
	def __init__(self, manager, data):
		super(Tag, self).__init__(data)
		self._manager=manager

	@property
	def manager(self):
	    return self._manager
	
	@property
	def channel(self):
	    return self.manager.channel

	@property
	def logger(self):
		return self.channel.logger
	
	def idstr(self):
		try:
			return '%s/%s/%s@%s' % (self.uuid, self.name, self.comment, self.manager.name)
		except:
			return ''

	def validateData(self, data):
		try:
			uuid=data['uuid']
			if uuid and (self.uuid is None or self.uuid==uuid):
				return True
		except:
			pass

	@property
	def uuid(self):
	    return self.get('uuid')

	@property
	def did(self):
	    return self.get('slaveId')
	
	@property
	def name(self):
	    return self.get('name')

	@property
	def comment(self):
	    return self.get('comment')

	@property
	def battery(self):
	    return max(self.get('batteryRemaining', 0.0), 1.0)

	@property
	def temperature(self):
	    return self.get('temperature', 0.0)

	@property
	def hygrometry(self):
	    return self.get('cap', 0.0)

	def isAlive(self):
		if self.get('alive') and not self.get('OutOfRange') and self.age()<15*60:
			return True

	# def __repr__(self):
	# 	return 'Tag(%s/%s/%s) %s' % (self.uuid, self.name, self.comment, str(self._data))

	def do(self, api, data):
		if self.manager.select():
			return self.channel.do(api, data)

	def beep(self, duration=1):
		if self.did is not None:
			return self.do(self.channel.apiEthClient('Beep'), {'id': self.did, 'beepDuration': int(duration)})

	def beepUntilMoved(self):
		return self.beep(1001)

	def beepUntilStopped(self):
		return self.beep(1000)

	def beepStop(self):
		if self.did is not None:
			return self.do(self.channel.apiEthClient('StopBeep'), {'id': self.did})

	def electBestTag(self, tag):
		if tag and isinstance(tag, Tag):
			if not self.isAlive() and not tag.isAlive():
				return None
			if self.isAlive() and not tag.isAlive():
				return self
			if tag.isAlive() and not self.isAlive():
				return tag
			if self.stampLastCommunication()>=tag.stampLastCommunication():
				return self
			return tag
		return self

		

class Channel(object):
	def __init__(self, authCode, logServer='localhost', logLevel=logging.DEBUG):
		self._authCode=authCode
		self._proxies=None
		requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
		self._managers={}
		self._managersIndexByName={}

		logger=logging.getLogger("WIRELESSTAG-%s" % self._authCode)
		logger.setLevel(logLevel)
		socketHandler = logging.handlers.SocketHandler(logServer, logging.handlers.DEFAULT_TCP_LOGGING_PORT)
		logger.addHandler(socketHandler)
		self._logger=logger

	@property
	def logger(self):
		return self._logger
    
	def setProxies(self, proxies):
		self._proxies=proxies

	def api(self, service, method):
		if service and method:
			return '%s/%s' % (service, method)

	def apiEthClient(self, method):
		return self.api('ethClient.asmx', method)

	def apiEthAccount(self, method):
		return self.api('ethAccount.asmx', method)

	def urlFromApi(self, api):
		if api:
			return '%s/%s' % (WIRELESSTAG_API_URL, api)

	def do(self, api, data=None):
		url=self.urlFromApi(api)
		if url and self._authCode:
			try:
				if not data:
					data={}

				self.logger.debug("%s(%s)" % (url, str(data)))

				headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % self._authCode}
				r=requests.post(url, headers=headers, 
					data=json.dumps(data), 
					proxies=self._proxies,
					verify=False,
					timeout=15.0)
				if r:
					if r.status_code==200:
						response=r.json()
						self.logger.debug(str(response))
						return response
					else:
						self.logger.exception('post()')
						#print r.status_code, r.text
			except:
				self.logger.exception('do()')
				pass

	def doAndGetData(self, api, data=None):
		try:
			return self.do(api, data)['d']
		except:
			pass

	def retrieveManagers(self):
		return self.doAndGetData(self.apiEthAccount('GetTagManagers'))

	def managers(self):
		try:
			return self._managers.values()
		except:
			pass

	def manager(self, mac):
		try:
			return self._managers[mac]
		except:
			pass

	def managerFromName(self, name):
		try:
			return self._managersIndexByName[name]
		except:
			pass

	def managerStore(self, data):
		try:
			mac=data['mac']
			if mac:
				manager=self.manager(mac)
				if manager:
					manager.update(data)
				else:
					manager=Manager(self, data)
					self._managers[manager.mac]=manager
					if manager.name:
						self._managersIndexByName[manager.name]=manager
				manager.read()
				return manager
		except:
			pass

	def read(self):
		managers=self.retrieveManagers()
		if managers:
			for data in managers:
				self.managerStore(data)
			return True

	def electBestTag(self, tags):
		if tags:
			tag=None
			for t in tags:
				tag=t.electBestTag(tag)
			return tag

	def tagFromName(self, name):
		tags=[]
		for manager in self.managers():
			tag=manager.tagFromName(name)
			if tag:
				tags.append(tag)
		return self.electBestTag(tags)

	def __getitem__(self, name):
		return self.tagFromName(name)


if __name__ == "__main__":
	pass


