#!/usr/bin/env python3

import os
import json

def _input(prompt, default):
	if len(default) == 0:
		return input(prompt)
	result = input('{} ({})'.format(prompt, default))
	return default if len(result) == 0 else result

def _reap_stanza(disk, extensions):
	return {
		"disk": disk,
		"percent" : "95",
		"extensions" : extensions
	}

print("PyNVR Configuration utility")
print("---------------------------")
print("This utility will ask a few questions and create a nvr.json file for you to use.")
print("")

base = input('Base Directory for storing files: ')

reaper = []

server_name = _input('Server name:', 'localhost')
server_port = _input('Server port:', '8080')
jpg_cache_dir = _input('Directory for storing temporary jpg files:', os.path.join(base, "working", "jpg"))
mp4_cache_dir = _input('Directory for storing temporary jpg files:', os.path.join(base, "working", "mp4"))
camera_logs_dir = _input('Directory for storing temporary jpg files:', os.path.join(base, "log"))
log_dir = _input('Directory for storing temporary jpg files:', os.path.join(base, "log"))

num = int(_input('How many cameras to configure:','1'))

reaper.append(_reap_stanza(jpg_cache_dir,["jpg"]))
reaper.append(_reap_stanza(mp4_cache_dir,["mp4"]))


cameras = []
for a in range(0,num):
	num = a + 1
	name = _input("Camera {} name:".format(num), "camera{}".format(num))
	url = _input("Url for Camera {}:".format(name), "")
	dst = _input("Path to store video for camera {} url:".format(name), os.path.join(base, "cameras", name))
	cameras.append({
		"enabled": True,
		"name" : name,
		"url" : url,
		"dst" : dst
	})
	reaper.append(_reap_stanza(dst,["mp4"]))
	


system = {
	"jpg_cache_dir" : jpg_cache_dir,
	"mp4_cache_dir" : mp4_cache_dir,
	"camera_log_dir" : camera_logs_dir,
	"log_dir" : log_dir,
	"server" : {
		"host" : server_name,
		"port" : int(server_port)
	}
}

data = {
	"system" : system,
	"cameras" : cameras,
	"reaper" : reaper
}

parsed = data

print("-----------------------------------")

default="./nvr-gen.json"

f = open(default, 'w')
f.write(json.dumps(parsed, indent=4, sort_keys=True))
f.close()

print("The file {} has been generated.  In order to use it, copy to /etc/nvr.json".format(default))

init="./pynvr.gen"

f = open(init, 'w')
f.write( "#!/bin/bash\n")
f.write( "pynvr.py $1\n")
f.close()
print("The file {} has been generated.  In order to use it, copy to /etc/init.d/pynvr".format(init))

