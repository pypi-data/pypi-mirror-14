#!/usr/bin/env python3

import logging
from shared import nvrconfig
from shared import reap
from shared import common
from shared.camera import Camera, minutesBetween, mergeRanges
from pprint import pprint
import threading
from datetime import datetime,timedelta
from subprocess import call,check_call
from bottle import route, run, template, static_file, HTTPError, request, response, install
from os import listdir
from os.path import isfile, join, exists, isdir
import glob
import os
import signal
import time
import subprocess
import sys
import atexit
import json
from shared import daemon

LOG_FILE="/tmp/pynvr.log"
PID_FILE="/tmp/pynvr.pid"


basepath = os.path.dirname(os.path.abspath(__file__))

if isdir(basepath + "/static"):
	static_dir = basepath + "/static"
else:
	static_dir = "/usr/share/pynvr/static"

#if 'PYTHONPATH' not in os.environ.keys() or len(os.environ['PYTHONPATH']) == 0:
	#print("ERROR : PYTHONPATH is not set, recording will not work without it pointing to pylive555/build/lib.linux-x86_64-3.4 or something similar.", file=sys.stderr)
	#exit(-1)

class MyDaemon(daemon.daemon):
	def __init__(self, pidfile, logger):
		daemon.daemon.__init__(self, pidfile)
		self.logger = logger
	def run(self):
		global reaper

		while True:

			self.logger.info("PyNVR - Python Network Video Recorder")
			self.logger.info("-------------------------------------")

			config_file = nvrconfig.locate_config_file('nvr.json')
			self.logger.info("config: {}".format(config_file))
			config = nvrconfig.parse(config_file, self.logger)

			if config == None:
				self.logger.error("There was a problem parsing the config file")
				exit(-1);

			common.setConfig(config)

			reaper = None

			class reaperThread(threading.Thread):
				def __init__(self, config, logger):
					threading.Thread.__init__(self)
					self.config = config
					self.done = False
					self.logger = logger
				def run(self):
					self.logger.info("Reaper starting . . .")
					while self.done == False:
						while reap.reap(self.config, logger) and self.done == False:
							True

						for a in range(0,60):
							time.sleep(.25)
							if self.done:
								break;
					self.logger.info("Reaper stopped.")
				def finish(self):
					self.done = True


			# This thread records a stream of data from a camera
			# If finish is called it kills it's spawned process and exits
			class recordThread (threading.Thread):
				def __init__(self, config, logger):
					threading.Thread.__init__(self)
					self.config = config
					self.done = False
					self.logger = logger
				def run(self):
					if 'initial_timeout' in self.config.keys():
						initial_timeout = self.config['initial_timeout']
					else:
						initial_timeout = 30
					if 'frame' in self.config.keys():
						frame_timeout = self.config['frame_timeout']
					else:
						frame_timeout = 5
					cmd = '{}/rtsp.py "{}" "{}" "{}" "{}" "{}" "{}" '.format(basepath, self.config['dst'],config['system']['jpg_cache_dir'],self.config['url'],self.config['id'], initial_timeout, frame_timeout)
					while self.done == False:
						self.logger.info("Starting record process for {}".format(self.config['id']))
						self.process = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
						while self.process.poll() is None and self.done == False:
							time.sleep(0.25)

						if (self.process.returncode != 0 and self.done == False):
							self.logger.error("There was a problem spawning the recording process for camera {}, return code is {}, trying again in a minute.".format(self.config['id'], self.process.returncode))
							for a in range(0,240):
								time.sleep(.25)
								if self.done:
									break;
				def finish(self):
					self.done = True
					try:
						os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
					except ProcessLookupError as e:
						self.logger.warn("Process not found: errno = {}, msg = {}".format(e.errno, e.strerror))	

			# Catch ctrl-c and shutdown nicely
			def signal_handler(signal, frame):
				global w
				global config
				self.logger.warn('You pressed Ctrl+C!')
				sys.exit(0)

			def exit_handler():
				global config
				self.logger.info('Shutting down')
				stopThreads(common.getConfig())

			atexit.register(exit_handler)
			signal.signal(signal.SIGINT, signal_handler)
			signal.signal(signal.SIGTERM, signal_handler)

			# Start all threads
			def startThreads(config):
				global reaper
				self.logger.info("Starting Recording Threads . . .")
				for camera in config['cameras']:
					if camera['enabled']:
						self.logger.info("starting camera: id = {}".format(camera['id']))
						thread = recordThread(camera, self.logger)
						thread.daemon = True
						thread.start()
						camera['_thread'] = thread

				if reaper == None:
					if 'reaper' in common.getConfig().keys():
						reaper = reaperThread(common.getConfig()['reaper'], self.logger)
						reaper.daemon = True
						reaper.start()

			def stopThreads(config):
				global reaper
				self.logger.info("Stopping Recording Threads . . .")
				for camera in config['cameras']:
					if camera['enabled']:
						if '_thread' in camera.keys():
							self.logger.info("stopping camera: id = {}".format(camera['id']))
							camera['_thread'].finish()
							camera.pop('_thread', None)
				if reaper != None:
					reaper.finish()
					reaper = None

				time.sleep(1)

			class  watcherThread(threading.Thread):
				def __init__(self):
					threading.Thread.__init__(self)
				def run(self):
					startThreads(common.getConfig())

					while [ True ]:
						start_mtime = os.stat(config_file).st_mtime
						while True:
							try:
								if start_mtime != os.stat(config_file).st_mtime:
									self.logger.info("config file change. reloading . . .\n")
									temp_config = nvrconfig.parse(config_file, self.logger)
									if (temp_config == None):
										self.logger.error("Config file changed, but could not be loaded, continuing with older config.")
										time.sleep(1)
									else:
										stopThreads(common.getConfig())
										config = temp_config
										common.setConfig(config)
										time.sleep(1)
										startThreads(config)
									break
							except FileNotFoundError as e:
								time.sleep(1)

			def payload(r):
				return json.dumps({ 'payload' : r, 'date': datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), 'system' : { 'name' : 'PyNVR', 'version' : '0.1' } })

			@route('/api/1/system.json')
			def system():
				running = True
				camera_status = {}
				for cam in config['cameras']:
					if cam['enabled']:
						value = Camera(common.getCameraConfig(cam['id'])).isRecording()
						camera_status[cam['id']] = value
						if not value:
							running = False


				r = { "status" : "running" if running else "error", "cameras" : camera_status }
				return payload(r)

			@route('/api/1/cameras.json')
			def cameras():
				r = []
				for cam in config['cameras']:
					if cam['enabled']:
						r.append(cam['id'])
				return payload(r)

			def fmt(d):
				return d.strftime("%Y%m%d.%H%M")


			@route('/api/1/camera/<camera_id>.json')
			def camera(camera_id):
				c = common.getCameraConfig(camera_id)

				video = c['dst']
				mp4s = [f for f in listdir(video) if isfile(join(video, f)) and f.endswith('mp4')]

				dates = [datetime.strptime(c, "{}.%Y%m%d.%H%M.mp4".format(camera_id)) for c in mp4s]
				dates.sort()

				ranges = []

				if len(dates) > 0:
					begin=min(dates)
					lastdate=begin
					for date in dates:
						diff = abs(lastdate - date)
						minutes=(int(diff.total_seconds()/60))
						if (minutes>1):
							ranges.append({ 'from' : fmt(begin), 'to' : fmt(lastdate) })
							begin=date
						lastdate = date

					if (begin != lastdate):
						ranges.append({ 'from' : fmt(begin), 'to' : fmt(lastdate) })

				r = { 
					"camera" : {
						"id" : camera_id,
						"enabled" : c['enabled'],
						"dates" : ranges
					}
				}
				return payload(r)

			@route('/api/1/camera/<camera_id>.preview.<YYYYMMDD>.<HHMM>.jpg')
			def camera_preview(camera_id, YYYYMMDD, HHMM):
				global config
				c = common.getCameraConfig(camera_id)
				jpg_filename = common.getJPGFilename(common.getConfig(), c, YYYYMMDD + "." + HHMM)

				return static_file(os.path.basename(jpg_filename), root = os.path.dirname(jpg_filename))

			@route('/api/1/camera/<camera_id>.thumbnail.<YYYYMMDD>.<HHMM>.jpg')
			def camera_thumbnail(camera_id, YYYYMMDD, HHMM):
				global config
				c = common.getCameraConfig(camera_id)
				jpg_filename = common.getJPGFilename(common.getConfig(), c, YYYYMMDD + "." + HHMM)
				if not os.path.isfile(jpg_filename):
					mp4_filename = common.getMP4Filename(c, YYYYMMDD + "." + HHMM)
					common.subprocess_mp4_to_jpg(mp4_filename, jpg_filename, None).wait()
				thumb_filename = common.getThumbnailFilename(common.getConfig(), c, YYYYMMDD + "." + HHMM)
				if not os.path.isfile(thumb_filename):
					common.subprocess_resize_jpg(jpg_filename, thumb_filename, "scale=320:-1").wait()

				return static_file(os.path.basename(thumb_filename), root = os.path.dirname(thumb_filename))

			@route('/api/1/camera/<camera_id>.<YYYYMMDD>.<HHMM>.mp4')
			def camera_mp4(camera_id, YYYYMMDD, HHMM):
				global config
				c = common.getCameraConfig(camera_id)
				mp4_filename = common.getMP4Filename(c, YYYYMMDD + "." + HHMM)

				return static_file(os.path.basename(mp4_filename), root = os.path.dirname(mp4_filename))

			@route('/api/1/camera/<camera_id>.range.<FROM_YYYYMMDD.HHMM>.to.<TO_YYYYMMDD.HHMM>.mp4')
			def camera_movie_range(camera_id, FROM_YYYYMMDD_HHMM, TO_YYYYMMDD_HHMM):
				c = common.getCameraConfig(camera_id)
				f = datetime.strptime(FROM_YYYYMMDD_HHMM, "%Y%m%d.%H%M")
				t = datetime.strptime(TO_YYYYMMDD_HHMM, "%Y%m%d.%H%M")
				mp4_filename = common.getMP4FilenameRange(common.getConfig(), c, FROM_YYYYMMDD_HHMM, FROM_YYYYMMDD_HHMM)

				files = []
				diff = int((t - f).total_seconds() / 60)
				for a in range(0,diff):
					d = f + timedelta(minutes = a)
					chunk_filename = common.getChunkFilename(c, d)
					if isfile(chunk_filename):
						files.append(chunk_filename)

					if len(files) > 60:
						raise HTTPError(413, "Time range too large, resulting movie would be too large")
						

				p = common.subprocess_chunks_to_mp4(basepath, files, mp4_filename)
				p.wait()

				return static_file(os.path.basename(mp4_filename), root = os.path.dirname(mp4_filename))

			@route('/api/1/cameras/<YYYYMMDD>')
			def camera_daily_info(YYYYMMDD):

				camera_ids = request.params['camera_ids']

				cameras = {}
				for camera_id in camera_ids.split(','):
					cameras[camera_id] = Camera(common.getCameraConfig(camera_id))

				dateRanges = []
				for camera_id in camera_ids.split(','):
					dateRanges.extend(cameras[camera_id].dateRangesForDay(datetime.strptime(YYYYMMDD,"%Y%m%d")))

				ranges = mergeRanges(dateRanges)

				if len(dateRanges) == 0:
					return payload({'dates' : [], 'min' : fmt(datetime.now()), 'max' : fmt(datetime.now()), 'camera_ids': camera_ids.split(',')})

				min_date = ranges[0].begin
				max_date = ranges[len(ranges)-1].end

				values = {} 
				for r in ranges:
					for d in minutesBetween(r):
						chunks = []
						for camera_id in camera_ids.split(','):
							chunk = cameras[camera_id].getChunk(d)
							if chunk != None:
								chunks.append(camera_id)
						values[fmt(d)] = chunks

				return payload({'dates' : values, 'min' : fmt(min_date), 'max' : fmt(max_date), 'camera_ids': camera_ids.split(',')})

			@route('/static/<path:path>')
			def static(path):
				return static_file(path, root = static_dir)

			@route('/')
			def index():
				return static_file("web.html", root = static_dir)

			w = watcherThread()
			w.daemon = True
			w.start()

			def plugin_logger(func):
				def wrapper(*args, **kwargs):
					global logger
					logger.info('%s %s %s %s %s' % (request.remote_addr, datetime.now().strftime('%H:%M'), request.method, request.url, response.status))
					req = func(*args, **kwargs)
					return req
				return wrapper

			install(plugin_logger)


			logger.info("starting bottle. . . ")
			run(host=config['system']['server']['host'], port=config['system']['server']['port'], quiet = True)

			time.sleep(10)


logger = logging.getLogger("pynvr")
#logger.setLevel(logging.INFO)
#formatter = logging.Formatter("%(ascitime)s - %(name)s - %(levelname)s - %(message)s")
#formatter = logging.Formatter("%(ascitime)s - %(name)s - %(levelname)s - %(message)s")
#handler = logging.FileHandler(LOG_FILE)
#handler.setFormatter(formatter)
#logger.addHandler(handler)

logging.basicConfig(filename=LOG_FILE,level=logging.DEBUG)



if __name__ == "__main__":
	daemon = MyDaemon('/tmp/pynvr.pid', logger)
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		elif 'status' == sys.argv[1]:
			daemon.status()
		elif 'foreground' == sys.argv[1]:
			ch = logging.StreamHandler(sys.stdout)
			ch.setLevel(logging.DEBUG)
			formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
			ch.setFormatter(formatter)
			logging.getLogger().addHandler(ch)

			daemon.run()
		else:
			print("Unknown command", file=sys.stderr)
			sys.exit(2)
		sys.exit(0)
	else:
		print("usage: {} start|stop|restart|foreground".format(sys.argv[0]), file=sys.stderr)
		sys.exit(2)
