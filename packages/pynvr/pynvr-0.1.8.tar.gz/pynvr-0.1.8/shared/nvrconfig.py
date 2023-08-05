#!/usr/bin/env python3
import json
import pprint
from os.path import isdir,exists
from shared import reap

def validate_dir(json, key, logger, error):
	if (key not in json.keys()):
		logger.error("key {} not found in stanza {}".format( key, json))
		return False

	if (not isdir(json[key])):	
		if error:
			logger.error('{} does not exists: {}'.format(key, json[key]))
			return False
		else:
			logger.error('{} does not exists: {}'.format(key, json[key]))

	return True

def locate_config_file(_filename):
	if (exists(_filename)):
		filename = _filename
	else:
		filename = "/etc/" + _filename
	return filename


def parse(filename, logger):
	data = {}

	with open(filename) as data_file:    
    		data = json.load(data_file)

	# Validate
	if 'system' not in data.keys():
		logger.error("no system stanza.")
		return None
	if 'server' not in data['system'].keys():
		logger.error("no system.server stanza.")
		return None
	if 'cameras' not in data.keys():
		logger.error("no cameras stanza.")
		return None

	s = data['system']

	if not validate_dir(data['system'],'jpg_cache_dir', logger, True):
		return None
	if not validate_dir(data['system'],'mp4_cache_dir', logger, True):
		return None
	if not validate_dir(data['system'],'camera_log_dir', logger, True):
		return None
	if not validate_dir(data['system'],'log_dir', logger, True):
		return None

	for camera in data['cameras']:
		if camera['enabled']:
			if not validate_dir(camera, 'dst', logger, True):
				return None

	if 'reaper' in data.keys():
		if (not reap.validate(data['reaper'], logger)):
			return None	

	return data


