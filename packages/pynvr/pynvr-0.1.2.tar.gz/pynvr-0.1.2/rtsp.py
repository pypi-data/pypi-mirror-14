#!/usr/bin/env python3

import logging
import time
import glob
import struct
import sys
import os
import re
import live555
import threading
from datetime import datetime
import subprocess
from shared import common

if len(sys.argv) != 7:
	print("ERROR : usage: rtsp.py chunk_path jpg_path url deviceid initial_timeout frame_timeout")
	exit(-1)


chunk_path = sys.argv[1]
jpg_path = sys.argv[2]
url = sys.argv[3]
deviceid = sys.argv[4]
initial_timeout = int(sys.argv[5])
frame_timeout = int(sys.argv[6])

logger = logging.getLogger("rtsp")
logging.basicConfig(filename="/tmp/{}.log".format(deviceid),level=logging.DEBUG)

basepath = os.path.dirname(os.path.abspath(__file__))

fixedurl = re.sub(r'rtsp:\/\/.*@', 'rtsp://........@', url, flags=re.IGNORECASE)
logger.info("Starting recording from {} to {} for {}".format(fixedurl, chunk_path,deviceid))

class createFrameThread(threading.Thread):
	def __init__(self, video, jpg, thumb, mp4):
		threading.Thread.__init__(self)
		self.video = video
		self.jpg = jpg
		self.thumb = thumb
		self.mp4 = mp4
	def run(self):
		global logger
		try:
			p2 = common.subprocess_chunk_to_mp4(basepath, self.video, self.mp4, "")
			p = common.subprocess_chunk_to_jpg(basepath, self.video, self.jpg, "")
			p.wait()
			p = common.subprocess_resize_jpg(self.jpg, self.thumb, "scale=320:-1")
			p.wait()
			p2.wait()
			os.remove(self.video)

			if os.stat(self.mp4).st_size < 4096:
				os.remove(self.mp4)
		except BaseException as e: 
			logger.error("CREATE FRAME THREAD - ", e)
		except:
			logger.error("CREATE FRAME THREAD - Something bad happend")


def createFrame(video, jpg, thumb, mp4):
	if video is None or len(video) == 0:
		return

	t = createFrameThread(video, jpg, thumb, mp4)
	t.start()
	return t

def record(chunk_path, jpg_path, url, deviceid, initial_timeout, frame_timeout):
	global logger

	now = datetime.now()
	chunk_filename = common.getChunkFilenameBy(chunk_path, deviceid, now)
	jpg_filename = common.getJPGFilenameBy(jpg_path, deviceid, now)
	thumb_filename = common.getThumbnailFilenameBy(jpg_path, deviceid, now)
	mp4_filename = common.getMP4FilenameBy(chunk_path, deviceid, now)

	state = {
		'lastfilename': "",
		'lastjpgfilename': "",
		'lastthumbfilename': "",
		'lastmp4filename': "",
		'fOut': open(chunk_filename, 'wb'),
		'filename': chunk_filename,
		'jpgfilename': jpg_filename,
		'thumbfilename': thumb_filename,
		'mp4filename': mp4_filename,
		'last_update': now,
		'first_update': True
	}

	# Cleanup and convert old chunk files for this camera into mp4's if done
	oldchunkfiles = glob.glob(os.path.join(chunk_path,"*/{}.*.*.chunk".format(deviceid)))
	if chunk_filename in oldchunkfiles: oldchunkfiles.remove(chunk_filename)
	for oldchunkfile in oldchunkfiles:
		logger.info("Upgrading {}".format(oldchunkfile))
		date_object = datetime.strptime(os.path.basename(oldchunkfile), "{}.%Y%m%d.%H%M.chunk".format(deviceid))
		old_jpg_filename = common.getJPGFilenameBy(jpg_path, deviceid, date_object)
		old_thumb_filename = common.getThumbnailFilenameBy(jpg_path, deviceid, date_object)
		old_mp4_filename = common.getMP4FilenameBy(chunk_path, deviceid, date_object)
		createFrame(oldchunkfile, old_jpg_filename, old_thumb_filename, old_mp4_filename).join()

	

	def oneFrame(codecName, bytes, sec, usec, durUSec, ctx):
		ctx['last_update'] = datetime.now()
		delta = datetime.now() - datetime(1970, 1, 1)
		frame_time = int(delta.total_seconds()*1000000)
		ctx['first_update'] = False

		F = int(bytes[0] & 128)
		NRI = int((bytes[0] & (64+32) ) / 32)
		TYPE = int((bytes[0] & (16+8+4+2+1) ))

		if TYPE==7:
			now = datetime.now()
			chunk_filename = common.getChunkFilenameBy(chunk_path, deviceid, now)
			jpg_filename = common.getJPGFilenameBy(jpg_path, deviceid, now)
			thumb_filename = common.getThumbnailFilenameBy(jpg_path, deviceid, now)
			mp4_filename = common.getMP4FilenameBy(chunk_path, deviceid, now)
			ctx['filename'] = chunk_filename
			ctx['jpgfilename'] = jpg_filename
			ctx['thumbfilename'] = thumb_filename
			ctx['mp4filename'] = mp4_filename

		if ctx['filename'] != ctx['lastfilename']:
			ctx['fOut'].close()
			createFrame(ctx['lastfilename'], ctx['lastjpgfilename'], ctx['lastthumbfilename'], ctx['lastmp4filename'])
			logger.info('INFO : opening {}'.format(ctx['filename']))
			ctx['fOut'] = open(ctx['filename'], 'wb')
			ctx['lastfilename'] = ctx['filename']
			ctx['lastjpgfilename'] = ctx['jpgfilename']
			ctx['lastthumbfilename'] = ctx['thumbfilename']
			ctx['lastmp4filename'] = ctx['mp4filename']


		ctx['fOut'].write(struct.pack('!BQQ', 0, frame_time, len(bytes)))
		ctx['fOut'].write(bytes)
		ctx['fOut'].flush()

		return ctx

	temp_oneFrame = lambda codecName, bytes, sec, usec, durUSec: oneFrame(codecName, bytes, sec, usec, durUSec, state)

	# Starts pulling frames from the URL, with the provided callback:
	useTCP = False
	live555.startRTSP(url, temp_oneFrame, useTCP)

	# Run Live555's event loop in a background thread:
	t = threading.Thread(target=live555.runEventLoop, args=())
	t.setDaemon(True)
	t.start()

	while True:
		delta = datetime.now() - state['last_update']
		time_since_update = delta.total_seconds()
		if state['first_update'] and time_since_update >= initial_timeout:
			logger.warn("Took longer than {} seconds for first frame".format(initial_timeout))
			break; 
		if state['first_update'] == False and time_since_update >= frame_timeout:
			logger.warn("Delay of over {} seconds for data".format(frame_timeout))
			break; 
		time.sleep(1)

	# Tell Live555's event loop to stop:
	live555.stopEventLoop()

	# Wait for the background thread to finish:
	t.join()

record(chunk_path, jpg_path, url, deviceid, initial_timeout, frame_timeout)

