# PyNVR - Python Network Video Recorder


## Goals:

The goal of this project is to provide a simple, yet powerful, network video recorder that can record high resolution h264 streams from multiple sources and archive it with minimal CPU usage.

This project is NOT designed to scan for motion events and alert when they are found. That may be added later, but for my usage, is not necessary. I find 99.99% of all motion events are not interesting. My typical usage is I see something has changed in view of my cameras, for example a large piece of trash appears, and I want to find out when it happened and who did it. I want to record as much as I can and be able to simply scrub the recorded video till I find the event. At that point, I want to download a mp4 that contains all relevant video data.

## TODO: (see future section)

- [ ] When Reaper stanza is missing in config, disable reaper
- [ ] Make camera retry timers configurable
- [ ] cleanup disk locations to simple configs are easy, e.g. a default location and structure along with default reaper config
- [ ] Add support for downloading mp4 files of arbitrary date ranges
- [ ] Add support for arching date ranges
- [ ] create debian package
- [ ] make a service that can be start/stopped easily
- [ ] get working on Raspberry Pi 3

## Config

See nvr.json.template for an example of the configuration file.

## Parts:

This project consists of three pieces in one service.  The main application is pynvr.py.

* Recorder Daemon - For each camera a rtsp.py process is spawned in the background to record from a single RTSP source. The recorder process will be restarted automatically on config file change.  The recorder process will try to connect to a RTSP source and save the data in mp4 files of 1 minute length.  Initially data is recorded in a temporary 'chunk' format.  When the minute is completed it is converted to a mp4 file.  When the mp4 for each minute is generated, a preview of the first frame of the video is generated as a jpg and also a smaller thumbnail of the same image is generated.  If the camera is unresponsive the connection is closed and retried.  A camera is considered unresponsive if we have never heard from it for over 30 seconds or if their is over a 5 second gap in data from an existing stream. The rstp.py process is build on top of pylive555 which is a Python wrapper around live555's rtsp library. Each camera can be configured to record to a different location on disk or a different disk. Currently only a single disk per camera can be used. 
* Reaper Daemon - Scans disk locations and deletes old video data in order to maintain enough free disk space for future recording. 
* Web - A simple web interface that can be used to see a list of cameras and see all recorded data for those cameras. Each video stream can be scrubbed at a minute granularity in order to preview the streams. Streams may be downloaded at a minute granularity in mp4 format or archived for future use.

## Technical:
We record streams for each camera in a custom wrapper format that produces a separate file per minute per camera. This allows us to delete or view data easily at a minute granularity. The container stores h264 NAL data that can be quickly and without loss converted to mp4 via FFmpeg.  These files only exists for short periods of time and are quickly converted to mp4 after they are complete.

The container format is very trivial:

* 1 byte - version, should be 0
* 8 bytes - 64 bit unsigned integer : length of block of data
* 8 bytes - 64 bit unsigned integer : time since epoch
* N bytes - h264 NAL frame data

Files are stored on disk in the form:

* {camera directory}/YYYYMMDD/$cameraid.YYYYMMDD.HHMM.chunk
* {camera directory}/YYMMDD/$cameraid.YYYYMMDD.HHMM.mp4


## Future:

### Archiving
Long term archiving and uploading to cloud storage. I have a compression format I have been designing for security video that I want to implement for archiving in this project. Archived data would be stored in something like Amazon Glacier storage at a hourly or daily granularity. 

### Tags
I may support motion events at some point and I would extend this to support arbitrary tags that external scripts could add to video. So beyond motion you might have tags like wind, animals, cars, and people.

## Installation

PyNVR is still in early stages and not really production ready.  But if you'd like to install it then here are the steps I used to install it on a fresh Ubuntu Linux install:

### Update packages we need and install them - python3, python3-pip, and git
`sudo apt-get update`
`sudo apt-get install python3 python3-pip git ffmpeg python-bottle`

### Download pynvr
`git clone https://gitlab.com/hoyle.hoyle/pynvr.git`

### Change into the pynvr directory
`cd pynvr`

### Download submodules
`git submodule init`
`git submodule update`

### Change into the pylive555 submodule directory
`cd pylive555`

### Download live555
`wget http://www.live555.com/liveMedia/public/live555-latest.tar.gz`

### Uncompress
`tar -xvzf live555-latest.tar.gz`

### Change into the live555 directory
`cd live`

### Replace linux-64bit with your OS type
`./genMakefiles linux-64bit`

### To build live555
`make`

### Go back into pylive555
`cd ..`	

### Edit the setup.py file (I use vi, you may use any editor you want)
`vi setup.py`

### Change the line 8 from this:
                   library_dirs=['%s/%s' % (INSTALL_DIR, x) for x in ['liveMedia', 'UsageEnvironment', 'groupsock']],
### to this:
                   library_dirs=['%s/%s' % (INSTALL_DIR, x) for x in ['liveMedia', 'UsageEnvironment', 'BasicUsageEnvironment', 'groupsock']],

### Build pylive555
`python3 setup.py build`

### Change back into pynvr directory
`cd ..`

### Set the PYTHONPATH to point to the library you just built. You can see this path in the output of building pylive555 above
`export PYTHONPATH=pylive555/build/lib.linux-x86_64-3.4`

### Take the nvr.json.template file and copy to nvr.json and edit
### If you don't know the URL to your camera try finding it here: https://www.soleratec.com/support/rtsp/rtsp_listing
`cp nvr.json.template nvr.json`
`vi nvr.json`

### WARNING WARNING

The reaper section of the config files will configure the system to automatically delete files when the disk starts to get full
Keep this section empty if you don't want this to occur.  When initially testing, it might be good to keep this empty until it makes sense for you.

### Start

Start the system, this will start recording of all enabled cameras along with starting the website on the defined interface/port
If you edit the nvr.json file while the system is running, it will reload the config file dynamically (fingers crossed!)

`./pynvr.py`


## Website

The website is still being built, but you can see it at http://localhost:8080/

## REST API Docs:


##### Endpoint: `GET /api/1/system.json`

Returns the current status of the system.  If everything is working as expected the key "status" will be "running", otherwise it will be "error". The cameras will be listed along with a boolean if they are currently recording successfully or not. Disabled cameras will not show up in this list.

Example:
```json
{
	"date" : "%Y-%m-%dT%H:%M:%S",
	"system" : { "name" : "PyNVR", "version" : "0.1" },
	"payload" : {
    	"status" : "running",
		"camera" : [ "camera1" : true, "camera2" : true ]
	}
}
 ```  

##### Endpoint: `GET /api/1/cameras.json`
List all enabled cameras in JSON

Example:
```json
{
	"date" : "%Y-%m-%dT%H:%M:%S",
	"system" : { "name" : "PyNVR", "version" : "0.1" },
	"payload": {
		"cameras" : [ "cam1", "cam2" ]
	}
}
 ```   

##### Endpoint: `GET /api/1/cameras/YYYYMMDD?camera_ids=<camera_id,camera_id,camera_id>`
List of all dates available for a specific camera

Example:
```json
{
	"date" : "%Y-%m-%dT%H:%M:%S",
	"system" : { "name" : "PyNVR", "version" : "0.1" },
	"payload" : {
		"min" : "YYYYMMDD.HHMM",
		"max" : "YYYYMMDD.HHMM",
		"camera_ids" : [ "camera1", "camera2", "camera3" ],
		"dates" : [ 
			"YYMMDD.HHMM" : [ "camera1", "camera2" ],
			"YYMMDD.HHMM" : [ "camera1", "camera2", "camera3" ],
			"YYMMDD.HHMM" : [ "camera1", "camera2", "camera3" ],
			"YYMMDD.HHMM" : [ "camera1", "camera2" ]
		]
	}
}
```


##### Endpoint: `GET /api/1/camera/$cameraid.preview.$YYMMDD.$HHMM.jpg`
Request a jpg for a camera representing the first frame of a date/time

##### Endpoint: `GET /api/1/camera/$cameraid.thumbnail.$YYMMDD.$HHMM.jpg`
Request a jpg for a camera representing a thumbnail first frame of a date/time

##### Endpoint: `GET /api/1/camera/$cameraid.preview.$YYMMDD.$HHMM.mp4`
Request a jpg for a camera representing up to a minute for a date/time

##### Endpoint: `GET /api/1/camera/$cameraid.range.$YYYYMMDD.$HHMM.to.$YYYYMMDD.$HHMM.mp4`
Request a video for a camera representing a time range

