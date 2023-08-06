"""
richtextpy.op

Copyright (c) 2016 Sachin Rekhi
"""

from copy import deepcopy
from type_utils import is_dict, is_string, NULL_STRING

def op_length(op):
	if 'insert' in op:
		return len(op['insert']) if is_string(op['insert']) else 1
	elif 'delete' in op:
		return op['delete']
	elif 'retain' in op:
		return op['retain']

def op_insert_string(op):
	if 'insert' in op:
		if is_string(op['insert']):
			return op['insert']
		else:
			return NULL_STRING

	raise Exception('Diff called on a non-document')

def attr_compose(a, b, keep_null):
	if not is_dict(a):
		a = dict()
	if not is_dict(b):
		b = dict()

	attributes = deepcopy(b)
	if not keep_null:
		for key in attributes.keys():
			if attributes[key] == None:
				del attributes[key]

	for key in a.keys():
		if key not in b:
			attributes[key] = a[key]
	
	if len(attributes.keys()) > 0:
		return attributes
	else:
		return None

def attr_transform(a, b, priority=True):
	if a == None:
		return b
	if b == None:
		return None
	if not priority:
		return b

	attributes = dict()
	for key in b.keys():
		if key not in a:
			attributes[key] = b[key]
	
	if len(attributes.keys()) > 0:
		return attributes
	else:
		return None

def attr_diff(a, b):
	if a == None:
		a = dict()
	if b == None:
		b = dict()

	attributes = dict()

	keys = a.keys() + b.keys()
	for key in keys:
		if a.get(key) != b.get(key):
			attributes[key] = None if b.get(key) == None else b[key]

	if len(attributes) > 0:
		return attributes
	else:
		return None
