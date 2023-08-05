import subprocess
import os
import platform
import glob
import time

def getPercent(filename, logger):
	try:
		df = subprocess.Popen(["df",filename], stdout=subprocess.PIPE)
		output = df.communicate()[0].decode(encoding='UTF-8').split("\n")[1].split()

		percent = "0%"
		mountpoint = None
		if (platform.system() == "Darwin"):
			device, blocks, used, available, percent, iused, ifree, percentiused, mountpoint = output
		elif (platform.system() == "Linux"):
			device, size, used, available, percent, mountpoint = output
		else:
			logger.error("unsupported system")
	
		percent = percent.split("%")[0]
	
		return percent,mountpoint
	except:
		return 0, None
	
def validate(config, logger):
	m = {}
	for p in config:
		disk = p['disk']
		percent = p['percent']
		actual_percent, mountpoint = getPercent(disk, logger)
		if mountpoint != None:
			if mountpoint in m.keys():
				if (percent != m[mountpoint]):
					logger.error("disk {} with different percent({} vs {}) on same mountpoint {} as other reap locations.".format(disk, percent, m[mountpoint], mountpoint))
					return False
			m[mountpoint] = percent
	return True

def reap(config, logger):
	if config == None:
		return False

	workDone = False

	# For a given mount point, find all locations and files
	filesToReap = {}

	for p in config:
		location = p['disk']
		trigger_percent = p['percent'].split("#")[0]
		extensions = p['extensions']

		percent, mountpoint = getPercent(location, logger)
		if mountpoint is None:
			continue

		# Remove empty directories
		dirs = [d for d in glob.glob(location + "/????????") if os.path.isdir(d)]
		for dir in dirs:
			if not os.listdir(dir):
				logger.info("removing empty directory {}".format(dir))
				os.rmdir(dir)

		if (int(percent) > int(trigger_percent)):
			files = []
			for ext in extensions:
				files.extend(glob.glob(location + "/????????/*." + ext))


			if mountpoint in filesToReap.keys():
				filesToReap[mountpoint].extend(files)
			else:
				filesToReap[mountpoint] = files


	for mountpoint, files in filesToReap.items():
		for i in range(0,5):
			if len(files)>0:
				workDone = True
				file = min(files, key=os.path.getctime)
				files.remove(file)
	
				logger.info("removing {}".format(file))
				os.remove(file)

	return workDone

