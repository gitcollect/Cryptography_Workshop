#!/usr/bin/env python

import pygst, threading, gobject, time
pygst.require("0.10")
import gst

_datalock = threading.Lock()
_data = ''
_dataevent = threading.Event()

def read(l=-1, timeout=False):
	global _datalock, _data, _dataevent

	r=''

	if l<0: # print buffer
		_datalock.acquire()
		r += _data
		_data = ''
		_dataevent.clear()
		_datalock.release()
		
	else: # wait for data
		t=time.time()

		while len(r)<l:
			remaining = l-len(r)

			_dataevent.wait(timeout)
			_datalock.acquire()
			r += _data[:remaining]
			_data = _data[remaining:]
			if len(_data)==0:
				_dataevent.clear()
			_datalock.release()

			if timeout and time.time()-t>timeout:
				break

	return r

def _handoff(element,buffer,pad):
	global _datalock, _data, _dataevent
	_datalock.acquire()
	_data += str(buffer)
	_dataevent.set()
	_datalock.release()

def record():
	_pipeline.set_state(gst.STATE_PLAYING)
def stop():
	_pipeline.set_state(gst.STATE_PAUSED)

_pipeline=gst.parse_launch('gconfaudiosrc ! capsfilter caps=audio/x-raw-int,rate=44100,channels=1,depth=16 ! fakesink name=sink signal-handoffs=true')

_pipeline.get_by_name('sink').connect('handoff', _handoff)

loop = gobject.MainLoop()
gobject.threads_init()

threading.Thread(target=loop.run).start()
