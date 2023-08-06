#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unicodedata

from marshmallow import (Schema, fields, post_load)

def remove_accents(input_str):
	nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
	return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

class ZohoError(Schema):
	
	message = fields.String()
	code = fields.Integer()

class ZohoFLObject(object):
	pass

class ZohoResponseObject(object):
		
	def __init__(self, data={}):
		if type(data) == dict:
			for key,value in data.items():

				if key == "FL":
					return_value = ZohoFLObject()
					for row in value:
						key_without_accents = remove_accents(row.get('val').replace(" ","_").lower())
						value_without_accents = remove_accents(row.get('content'))

						setattr(return_value, key_without_accents, value_without_accents)

					setattr(self, key, return_value)

				else:
					if type(value) == dict:
						setattr(self, key, ZohoResponseObject(value))

					elif type(value) == list:
						for row in value:
							if type(row) == dict:
								setattr(self, key, ZohoResponseObject(row))
							else:
								setattr(self, key, value)

					else:
						setattr(self, key, value)
		
		elif type(data) == list:
			for row in data:
				if type(row) == dict:
					for k,v in row.items():
						setattr(self, k, ZohoResponseObject(v))
				else:
					setattr(self, key, value)



class ZohoResponse(Schema):

	error = fields.Dict(default={})
	uri = fields.String(default="")
	result = fields.Dict(default={})

	@post_load(pass_many=False)
	def convert_to_obj(self, data):
		obj_to_response = ZohoResponseObject(data=data)
		return obj_to_response
