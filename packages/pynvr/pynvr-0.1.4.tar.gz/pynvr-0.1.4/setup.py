from setuptools import setup, find_packages, Extension

import os

INCLUDE_DIR = '/usr/include'
INSTALL_DIR = './live'
dirs=['%s/%s' % (INCLUDE_DIR, x) for x in ['liveMedia', 'BasicUsageEnvironment', 'UsageEnvironment', 'groupsock']]
dirs.extend(['%s/%s/include' % (INSTALL_DIR, x) for x in ['liveMedia', 'BasicUsageEnvironment', 'UsageEnvironment', 'groupsock']])
module = Extension('live555',
                   include_dirs=dirs,
                   libraries=['liveMedia', 'groupsock', 'BasicUsageEnvironment', 'UsageEnvironment'],
                   #extra_compile_args = ['-fPIC'],
                   library_dirs=['%s/%s' % (INSTALL_DIR, x) for x in ['liveMedia', 'UsageEnvironment','BasicUsageEnvironment', 'groupsock']],
                   sources = ['pylive555/module.cpp'])

setup(
	name = "pynvr",
	version = "0.1.4",
	description = "Network Video Recorder for recording h264 rtsp IP cameras",
	author = "Jack Strohm",
	author_email = "hoyle.hoyle@gmail.com",
	url = "https://gitlab.com/hoyle.hoyle/pynvr",
	license = "MIT",
	packages = find_packages(),
	scripts = ['pynvr.py', 'rtsp.py', 'extract_h264.py'],
	install_requires = ['bottle>=0.12'],
	include_package_data = True,
	package_data = {
		'': ['*.txt', '*.rst', '*.md'],
		'static': ['*.html','*.png', '*.css', '*.gif', '*.html', '*.js', '*.png' ],
	},
	ext_modules = [module],
	keywords = ['nvr', 'security', 'recording', 'ip camera', 'rtsp', 'h264', 'camera'],
)

