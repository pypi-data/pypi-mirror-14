import os

_STATIC_ROOT = os.path.abspath(os.path.dirname(__file__))

def get_static_root():
	return _STATIC_ROOT
