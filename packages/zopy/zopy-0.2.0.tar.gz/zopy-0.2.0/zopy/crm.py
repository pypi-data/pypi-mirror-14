#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from core import (Connection,ZohoException)

class CRM(Connection):

	def __init__(self, **kwargs):
		for key,value in kwargs.items():
			setattr(self, key, value)
		super(CRM, self).__init__()

	""" To retrieve data by the owner of the Authentication Token specified in the API request """
	def getMyRecords(self, module=None, **options):
		action = "getMyRecords"
		params = self._options_to_params(authToken=self.authToken,
			scope=self.scope, options=options)

		return self._getPost( module=module, 
			action=action, options=options)

	""" To insert records into the required Zoho CRM module """
	def insertRecords(self, xmlData=[], module=None, **options):
		action = "insertRecords"
		xml = self.prepare_xml(module=module, leads=xmlData)
		return self._getPost( module=module ,xml=xml, 
			action=action, options=options)

	def searchRecords(self, module=None, criteria={}, **options):
		action="searchRecords"
		if not criteria or type(criteria) is not dict:
			raise ZohoException("You must set a valid criteria dictionary")

		criteria_str = "("
		for k,v in criteria.items():
			criteria_str += "{}:{}".format(k,v)
		criteria_str += ")"

		options.update({"criteria":criteria_str})

		return self._getPost( module=module, 
			action=action, options=options)

	def updateRecords(self, module=None, id=None, xmlData=None, **options):
		action="updateRecords"
		options.update({"id":id})

		xml = self.prepare_xml(module=module, leads=xmlData)
		return self._getPost( module=module ,xml=xml, 
			action=action, options=options)