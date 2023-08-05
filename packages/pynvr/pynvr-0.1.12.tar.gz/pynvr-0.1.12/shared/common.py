import subprocess
import os
import glob
import platform
from shared import nvrconfig

prereqs_msg = ""
ffmpeg_path = None

def subprocess_mp4_to_jpg(mp4, jpg, options):
	cmd = "{} -i {} -vframes 1 {} 2>/dev/null 1>/dev/null".format(ffmpeg_path, mp4, jpg)
	return subprocess.Popen(cmd, shell=True)

def subprocess_chunk_to_jpg(basepath, chunk, jpg, options):
	cmd = "{}/extract_h264.py {} | {} -f h264 -r 30 -i - -vcodec copy  -f mpegts - 2>/dev/null | {} -r 30 -i - -vframes 1 -f {} image2 {} 2>/dev/null 1>/dev/null".format(basepath, chunk, ffmpeg_path, ffmpeg_path, options, jpg)
	return subprocess.Popen(cmd, shell=True)

def subprocess_chunk_to_mp4(basepath, chunk, mp4, options):
	cmd = "{}/extract_h264.py {} | {} -f h264 -r 30 -i - -vcodec copy  -f mp4 {} -movflags +faststart 2>/dev/null".format(basepath, chunk, ffmpeg_path, mp4)
	return subprocess.Popen(cmd, shell=True)

def subprocess_resize_jpg(from_jpg, to_jpg, options):
	# scale=320:-1
	cmd = "{} -i {} -vf {} {} 2>/dev/null".format(ffmpeg_path, from_jpg, options, to_jpg)
	return subprocess.Popen(cmd, shell=True)

def subprocess_chunks_to_mp4(basepath, chunks, mp4):
	cmd = "{}/extract_h264.py {} | {} -f h264 -r 30 -i - -vcodec copy  -f mp4 -movflags +faststart {} 2>/dev/null".format(basepath, ' '.join(str(x) for x in chunks), ffmpeg_path, mp4)
	return subprocess.Popen(cmd, shell=True)

def subprocess_mp4s_to_mp4(basepath, mp4s, mp4):
	temp = "concat:" + '|'.join(mp4s)
	cmd = '{} -y -i "{}" -c copy {}'.format(ffmpeg_path, temp, mp4)
	print(cmd)
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

def getRangeFilesForCamera(camera_id):
	global config
	d = config['system']['mp4_cache_dir']
	return glob.glob("{}/{}.range.*.*.mp4".format(d, camera_id))

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

def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def check_prereqs():
	global ffmpeg_path, prereqs_msg
	ffmpeg1 = which("ffmpeg") 
	ffmpeg_path = ffmpeg1 if ffmpeg1 != None else which("ffmpeg.exe")

	if ffmpeg_path == None:
		prereqs_msg = prereqs_msg + "ffmpeg was not found on the path, perhaps it isn't installed? "

	if len(nvrconfig.locate_config_file('nvr.json')) == 0:
		prereqs_msg = prereqs_msg + "Could not locate nvr.json.  It must be in the current directory or at /etc/nvr.json"

	return True if len(prereqs_msg) == 0 else False

def get_prereqs_msg():
	return prereqs_msg

def get_ffmpeg_path():
	return ffmpeg_path
	
	
