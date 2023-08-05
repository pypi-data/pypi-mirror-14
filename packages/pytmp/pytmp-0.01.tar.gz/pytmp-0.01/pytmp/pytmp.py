
import shelve
import os

DEFAULT_PATH_FILE = '/tmp/tmp.shelve'


def tmp_create(key, value=None, name_file=DEFAULT_PATH_FILE):
	"""Method to create value in temp file"""
	tmp_file = shelve.open(name_file, writeback=True)
	tmp_file[key] = value
	tmp_file.close()
	return tmp_read(key)


def tmp_clear(name_file=DEFAULT_PATH_FILE):
	"""Method to clear all values in temp file"""
	tmp_file = shelve.open(name_file, writeback=True)
	
	for k in list(tmp_file.keys()):
		del tmp_file[k]

	tmp_file.close()
	return tmp_keys()


def tmp_update(key, new_value=None, name_file=DEFAULT_PATH_FILE):
	"""Method to update value based in keys"""
	tmp_create(key, new_value, name_file)
	return tmp_read(key)


def tmp_delete(key, name_file=DEFAULT_PATH_FILE, debug=False):
	"""Method to delete value based in key"""
	result, tmp_file = False, shelve.open(name_file, writeback=True)

	try:
		del tmp_file[key]
		result = True
	except Exception as e:
		print('except: %s' % e) if debug == True else None

	tmp_file.close()
	return result


def tmp_read(key, name_file=DEFAULT_PATH_FILE):
	"""Method to get a key value in temp file"""
	tmp_file = shelve.open(name_file, writeback=True)
	value_from_tmp_file = tmp_file.get(key)

	tmp_file.close()
	return value_from_tmp_file


def tmp_keys(name_file=DEFAULT_PATH_FILE):
	"""Method to return keys in temp file"""
	tmp_file = shelve.open(name_file, writeback=True)
	keys_from_tmp_file = list(tmp_file.keys())

	tmp_file.close()
	return keys_from_tmp_file


def tmp_items(name_file=DEFAULT_PATH_FILE):
	"""Method to return items in temp file"""
	tmp_file = shelve.open(name_file, writeback=True)
	items_from_tmp_file = list(tmp_file.items())	

	tmp_file.close()
	return items_from_tmp_file

