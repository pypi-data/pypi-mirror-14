import subprocess
import os

def subprocess_mp4_to_jpg(mp4, jpg, options):
	cmd = "ffmpeg -i {} -vframes 1 {} 2>/dev/null 1>/dev/null".format(mp4, jpg)
	#cmd = "ffmpeg -i {} -vcodec copy  -f mpegts - | ffmpeg -r 30 -i - -vframes 1 -f {} image2 {}".format(mp4, options, jpg)
	return subprocess.Popen(cmd, shell=True)

def subprocess_chunk_to_jpg(basepath, chunk, jpg, options):
	cmd = "{}/extract_h264.py {} | ffmpeg -f h264 -r 30 -i - -vcodec copy  -f mpegts - 2>/dev/null | ffmpeg -r 30 -i - -vframes 1 -f {} image2 {} 2>/dev/null 1>/dev/null".format(basepath, chunk, options, jpg)
	return subprocess.Popen(cmd, shell=True)

def subprocess_chunk_to_mp4(basepath, chunk, mp4, options):
	cmd = "{}/extract_h264.py {} | ffmpeg -f h264 -r 30 -i - -vcodec copy  -f mp4 {} -movflags +faststart 2>/dev/null".format(basepath, chunk, mp4)
	return subprocess.Popen(cmd, shell=True)

def subprocess_resize_jpg(from_jpg, to_jpg, options):
	# scale=320:-1
	cmd = "ffmpeg -i {} -vf {} {} 2>/dev/null".format(from_jpg, options, to_jpg)
	return subprocess.Popen(cmd, shell=True)

def subprocess_chunks_to_mp4(basepath, chunks, mp4):
	cmd = "{}/extract_h264.py {} | ffmpeg -f h264 -r 30 -i - -vcodec copy  -f mp4 -movflags +faststart {} 2>/dev/null".format(basepath, ' '.join(str(x) for x in chunks), mp4)
	return subprocess.Popen(cmd, shell=True)

def _date_string(temp_date):
	if (type(temp_date) is str):
		return temp_date
	return temp_date.strftime("%Y%m%d.%H%M")

def _dir_string(temp_date):
	if (type(temp_date) is str):
		return temp_date.split(".")[0]
	return temp_date.strftime("%Y%m%d")

def get_dated_dir(temp_dir, temp_date):
	directory = os.path.join(temp_dir, _dir_string(temp_date))
	if not os.path.exists(directory):
		os.makedirs(directory)
	return directory
	

def getChunkFilename(camera, temp_date):
	return get_dated_dir(camera['dst'], temp_date) + "/{}.{}.chunk".format(camera['id'],_date_string(temp_date))
def getChunkFilenameBy(path, camera_id, temp_date):
	return get_dated_dir(path,temp_date) + "/{}.{}.chunk".format(camera_id,_date_string(temp_date))

def getJPGFilename(config, camera, temp_date):
	d = get_dated_dir(config['system']['jpg_cache_dir'],temp_date)
	return "{}/{}.preview.{}.jpg".format(d, camera['id'],_date_string(temp_date))
def getJPGFilenameBy(path, camera_id, temp_date):
	return "{}/{}.preview.{}.jpg".format(get_dated_dir(path,temp_date), camera_id,_date_string(temp_date))

def getThumbnailFilename(config, camera, temp_date):
	d = get_dated_dir(config['system']['jpg_cache_dir'],temp_date)
	return "{}/{}.thumbnail.{}.jpg".format(d, camera['id'],_date_string(temp_date))
def getThumbnailFilenameBy(path, camera_id, temp_date):
	return "{}/{}.thumbnail.{}.jpg".format(get_dated_dir(path, temp_date), camera_id,_date_string(temp_date))

def getMP4Filename(camera, temp_date):
	return "{}/{}.{}.mp4".format(get_dated_dir(camera['dst'],temp_date), camera['id'],_date_string(temp_date))
def getMP4FilenameBy(path, camera_id, temp_date):
	return "{}/{}.{}.mp4".format(get_dated_dir(path, temp_date), camera_id,_date_string(temp_date))

def getMP4FilenameRange(config, camera, temp_from_date, temp_to_date):
	d = config['system']['mp4_cache_dir']
	return "{}/{}.range.{}.to.{}.mp4".format(d, camera['id'],_date_string(temp_from_date), _date_string(temp_to_date))
def getMP4FilenameRangeBy(path, camera_id, temp_from_date, temp_to_date):
	return "{}/{}.range.{}.to.{}.mp4".format(path, camera['id'],_date_string(temp_from_date), _date_string(temp_to_date))

def getCameraConfig(camera_id):
	global config
	for cam in config['cameras']:
		if cam['id'] == camera_id:
			return cam
	return None

config = None

def setConfig(c):
	global config
	config = c

def getConfig():
	return config
