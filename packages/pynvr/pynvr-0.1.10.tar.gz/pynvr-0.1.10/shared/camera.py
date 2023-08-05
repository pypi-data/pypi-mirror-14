import re
import os
import glob
import time
from datetime import datetime,timedelta
from os import listdir
from collections import namedtuple
from shared import common
from datetime import datetime,timedelta

DateRange = namedtuple("DateRange", "begin end")
Chunk = namedtuple("Chunk", "mp4 jpg thumbnail date")

def minutesBetween(daterange):
	dates = []

	diff = int((daterange.end - daterange.begin).total_seconds() / 60)
	for a in range(0,diff+1):
		dates.append(daterange.begin + timedelta(minutes = a))

	return dates

def rangesFromDates(dates):
	ranges = []

	if dates != None and len(dates) > 0:
		dates = set(dates)
		dates = list(dates)
		dates.sort()

		begin = min(dates)
		lastdate = begin
		for date in dates:
			diff = abs(lastdate - date)
			minutes = int(diff.total_seconds()/60)
			if minutes > 1:
				ranges.append(DateRange(begin, lastdate))
				begin = date
			lastdate = date

		ranges.append(DateRange(begin,lastdate))

	return ranges

def mergeRanges(ranges):

	dates = []

	for range in ranges:
		dates.extend(minutesBetween(range))

	return rangesFromDates(dates)




class Camera:
	def __init__(self, config):
		self.config = config
		self.enabled = config['enabled']
		self.url = config['url']
		self.path = config['dst']
		self.camera_id = config['id']

	def cameraMP4s(self):
		return glob.glob(os.path.join(self.path,"/*/{}.*.*.mp4".format(self.camera_id)))

	def cameraMP4sForHour(self,date):
		return glob.glob(os.path.join(common.get_dated_dir(self.path,date),"{}.{}??.mp4".format(self.camera_id, date.strftime("%Y%m%d.%H"))))

	def cameraMP4sForDay(self,date):
		return glob.glob(os.path.join(common.get_dated_dir(self.path,date),"{}.{}.????.mp4".format(self.camera_id, date.strftime("%Y%m%d"))))

	def getChunk(self, date):
		mp4 = common.getMP4Filename(self.config, date)
		#if not os.path.isfile(mp4):
			#mp4 = None

		jpg = common.getJPGFilename(common.config, self.config, date)
		#if not os.path.isfile(jpg):
			#jpg = None

		thumbnail = common.getThumbnailFilename(common.config, self.config, date)
		#if not os.path.isfile(thumbnail):
			#thumbnail = None

		if mp4 == None and jpg == None and thumbnail == None:
			return None

		return Chunk(mp4, jpg, thumbnail, date)

	def dateRanges(self):
		mp4s = self.cameraMP4s()
		dates = [datetime.strptime(os.path.basename(c), "{}.%Y%m%d.%H%M.mp4".format(self.camera_id)) for c in mp4s]

		return rangesFromDates(dates)

	def dateRangesForHour(self, date):
		mp4s = self.cameraMP4sForHour(date)
		dates = [datetime.strptime(os.path.basename(c), "{}.%Y%m%d.%H%M.mp4".format(self.camera_id)) for c in mp4s]
		return rangesFromDates(dates)

	def dateRangesForDay(self, date):
		mp4s = self.cameraMP4sForDay(date)
		dates = [datetime.strptime(os.path.basename(c), "{}.%Y%m%d.%H%M.mp4".format(self.camera_id)) for c in mp4s]
		return rangesFromDates(dates)

	def maskedURL(self):
		return re.sub(r'rtsp:\/\/.*@', 'rtsp://........@', self.url, flags=re.IGNORECASE)

	def URL(self):
		return self.url

	def isRecording(self):
		chunks = glob.glob(os.path.join(self.path,"*/{}.*.*.chunk".format(self.camera_id)))
		chunks = [a for a in chunks if os.stat(a).st_size != 0]
		if len(chunks) == 0:
			return False

		dates = [datetime.strptime(os.path.basename(c), "{}.%Y%m%d.%H%M.chunk".format(self.camera_id)) for c in chunks]
		dates.sort()
		end = max(dates)

		d1_ts = time.mktime(end.timetuple())
		d2_ts = time.mktime(datetime.now().timetuple())
		minutes = int(d2_ts-d1_ts) / 60

		return minutes < 2
