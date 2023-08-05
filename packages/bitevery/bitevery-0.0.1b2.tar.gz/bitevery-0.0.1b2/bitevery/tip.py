from . import apiUtil
from apiUtil import *

class tipService:
	_FORMAT = None
	_LOCALE = None
	_TIP_ENDPOINT = "tip"
	_SEPARATOR = "/"	
	
	def getFormat(self):
		return self._FORMAT
	
	def setFormat(self, format):
		self._FORMAT = str(format)
	
	def getLocale(self):
		return self._LOCALE	
	
	def setLocale(self, locale):
		self._LOCALE = str(locale)

	@staticmethod
	def getResourceString(action):
		return tipService._TIP_ENDPOINT + tipService._SEPARATOR + action
	
	@staticmethod
	def paramToList(params):
		output = []
		for key in params:
			keyValue = str(key) + "=" + str(params[key])
			output.append(keyValue)
		return output
		
	def getTipLink(self, api_code, **distribution):
		resource = tipService.getResourceString("tip_link")
		params = {}
		if(self.getFormat() is not None):
			params["format"] = self.getFormat()
		if(self.getLocale() is not None):
			params["locale"] = self.getLocale()
			
		if(len(distribution) == 0):
			return self.__getTipLinkSingleReceivers(resource, api_code, params)
		else:
			return self.__getTipLinkMultipleReceivers(resource, api_code, params, distribution)
	
	def __getTipLinkSingleReceivers(self, resource, api_code, params):
		if(len(params) == 0):
			return call_api(resource, api_code)
		else:
			return call_api(resource, api_code, tipService.paramToList(params))
			
	def __getTipLinkMultipleReceivers(self, resource, api_code, params, distribution):
		params.update(distribution);
		return call_api(resource, api_code, tipService.paramToList(params))