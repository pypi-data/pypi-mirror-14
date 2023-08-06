#!/usr/bin/env python
# -*- coding: utf-8 -*-
from schemas import ZohoResponse

from xml import etree
from xml.etree.ElementTree import Element, tostring, fromstring, SubElement

import requests

class ZohoException(Exception):
	pass

class Properties(object):
	
	# Set properties
	@property
	def user(self):
		try:
			return self._user
		except AttributeError:
			self._user = None
			return self._user

	@user.setter
	def user(self, value):
		self._user = value
	
	@property
	def password(self):
		try:
			return self._password
		except AttributeError:
			self._password = None
			return self._password

	@password.setter
	def password(self, value):
		self._password = value

	@property
	def scope(self):
		try:
			return self._scope
		except AttributeError:
			self._scope = "ZohoCRM/crmapi"
			return self._scope

	@scope.setter
	def scope(self, value):
		self._scope = value
	
	@property
	def app_name(self):
		try:
			return self._app_name
		except AttributeError:
			self._app_name = None
			return self._app_name

	@app_name.setter
	def app_name(self, value):
		self._app_name = value

	@property
	def authToken(self):
		try:
			return self._authToken
		except AttributeError:
			self._authToken = None
			return self._authToken
	@authToken.setter
	def authToken(self, value):
		self._authToken = value

	@property
	def module(self):
		try:
			return self._module
		except AttributeError:
			self._module = None
			return self._module

	@module.setter
	def module(self, value):
		self._module = value

class Connection(Properties):

	def __init__(self, **kwargs):
		for key,value in kwargs.items():
			setattr(self, key, value)

		self.tokenURL = "https://accounts.zoho.com/apiauthtoken/nb/create?SCOPE={scope}&EMAIL_ID={user}&PASSWORD={password}&DISPLAY_NAME={app_name}"
		self.url = "https://crm.zoho.com/crm/private/json/{module}/{action}?{params}"
		
		super(Connection, self).__init__()

	def _valid_mandatory_fields(self, authToken=None, scope=None, module=None):

		if authToken is not None:
			self.authToken = authToken
		elif authToken is None and self.authToken is None:
			raise ZohoException("You have to assing an authToken")

		if scope is not None:
			self.scope = scope
		elif scope is None and self.scope is None:
			raise ZohoException("You have to assing a scope")

		if module is not None:
			self.module = module
		elif module is None and self.module is None:
			raise ZohoException("You have to assing a module")

	def _valid_data_login(self):
		if self.user == None:
			raise AttributeError("You need to set a Username/EmailID")
		elif self.password == None:
			raise AttributeError("You need to set a Password")
		elif self.app_name == None:
			raise AttributeError("You need to set an ApplicationName")

	def _options_to_params(self, authToken=None, scope=None, xml=[], options={}):
		params_string = "authtoken={}&scope={}&".format(authToken,scope)
		
		for k,v in options.items():
			
			if type(v) is list:
				params_string += "{}={}(".format(k,self.module)
				for i in v:
					params_string += i
				params_string = params_string[:-1]
				params_string += ")&"

			else:	
				params_string += "{}={}&".format(k,v)

		if xml:
			params_string += "xmlData={}".format(xml)
		else:
			params_string = params_string[:-1]
		
		return params_string

	def _getPost(self, module=None ,xml=None, action=None, options={}):
		params = self._options_to_params(authToken=self.authToken,
			scope=self.scope, xml=xml, options=options)

		url = self.url.format(module=module,action=action,params=params)		
		response_json = requests.get(url).json()
		return ZohoResponse(many=False).load(response_json.get('response')).data
	
	def createAuthToken(self):
		try:
			self._valid_data_login()
		except AttributeError as e:
			raise e
		else:
			url = self.tokenURL.format(scope=self.scope, 
				user = self.user,
				password = self.password,
				app_name = self.app_name)

			zoho_response = requests.get(url)
			
			zoho_authToken = [z for z in zoho_response.text.split("\n") if "AUTHTOKEN" in z]
			zoho_authToken = zoho_authToken[0].replace("AUTHTOKEN=","")

			if "CAUSE" in zoho_authToken:
				raise ZohoException("Exceeded Maximum Allowed AuthTokens")
			self.authToken = zoho_authToken
		return zoho_authToken

	def prepare_xml(self, module, leads):
		root = Element(module)		
		no = 1
		for lead in leads:
			row = Element("row", no=str(no))
			root.append(row)
			if type(lead) == dict:			
				for key, value in lead.items():
					fl = Element("FL", val=key.decode("utf-8"))
					if type(value) != str:
						try:
							fl.text = str(value)
						except:
							fl.text = ""
					else:
						fl.text = value.decode("utf-8")
					row.append(fl)
				no += 1

		return tostring(root, encoding='UTF-8')
