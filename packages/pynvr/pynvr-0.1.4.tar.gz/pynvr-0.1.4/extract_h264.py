#!/usr/bin/env python3

import time
import struct
import sys

out = False
if len(sys.argv) == 1:
	print(file=sys.stderr)
	print('Usage: python3 extract_h264.py fileIn [... more files]', file=sys.stderr)
	print(file=sys.stderr)
	sys.exit(1)

for i in range(1, len(sys.argv)):
	fileIn = sys.argv[1]

	fIn = open(fileIn,'rb')

	while True:
		try:
			zero, time, length = struct.unpack('!BQQ', fIn.read(17))
			data = fIn.read(length)
			sys.stdout.buffer.write(b'\0\0\0\1' + data)
		except:
			break;
	
	fIn.close()

